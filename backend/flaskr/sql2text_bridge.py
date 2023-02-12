import traceback
from typing import Tuple, List
from flask import current_app
from flaskr import file_utils
from flaskr.evaluation_result import EvaluationResult

import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

from Data.dataset import SeqDataset, TreeDataset, RGTDataset
from Data.utils import get_seq_batch_data, get_tree_batch_data, get_RGT_batch_data
from Data.vocab import Vocabulary
from Model.model import AbsoluteTransformer, RelativeTransformer, BiLSTM, TreeLSTM, RGT
from Utils.const import TYPE_NUM, UP_TYPE_NUM, DOWN_TYPE_NUM, UP_SCHEMA_NUM
from Utils.metric import get_metric

MAX_DECODE = 500
TRAIN_SEQ_DATASET_KEY = "train_seq_dataset"
TRAIN_TREE_DATASET_KEY = "train_tree_dataset"
TRAIN_RGT_DATASET_KEY = "train_rgt_dataset"
TRAIN_TABLE_FILE_PATH = "Dataset/spider/tables.json"

MODEL_BILSTM = "BiLSTM"
MODEL_TRANSFORMER = "ABS"
MODEL_RELATIVE_TRANSFORMER = "REL"
MODEL_TREELSTM = "TreeLSTM"
MODEL_RGT = "RGT"

# contains name abbreviations of all supported models
SUPPORTED_MODELS = [MODEL_BILSTM, MODEL_TRANSFORMER,
                    MODEL_RELATIVE_TRANSFORMER, MODEL_TREELSTM, MODEL_RGT]
TRAIN_DATA_FILES = [
    "Dataset/spider_composed/train.json",
]

device = torch.device("cuda:0")
train_seq_dataset: Dataset = None
train_tree_dataset: Dataset = None
train_rgt_dataset: Dataset = None
checkpoint_dict: dict = {}


def predict(model_name: str, db_id: str, gold_nl_array: str, input_sql: str, input_identifier: str) -> EvaluationResult:
    result = EvaluationResult()
    result.modelName = model_name
    result.original = input_sql
    # score is considered only gold_nl is passed in
    result.hasScore = gold_nl_array != None and gold_nl_array != ""

    if model_name not in SUPPORTED_MODELS:
        error_msg = f"model '{model_name}' is not in supported models {SUPPORTED_MODELS}!"
        current_app.logger.error(error_msg)
        result.failedReason = error_msg
        return result

    # current_app.logger.info(f"you are on bridge, torch version:{torch.__version__}")
    input_identifier = f"{input_identifier}.{model_name}"
    jsonTargetPath = file_utils.build_input_sql_json(
        db_id, gold_nl_array, input_sql, input_identifier)
    if jsonTargetPath == "":
        error_msg = f"build json file for model '{model_name}' input_sql '{input_sql}' failed!"
        current_app.logger.error(error_msg)
        result.failedReason = error_msg
        return result

    run_sql2text(model_name, jsonTargetPath, result)
    return result


def is_ready():
    return len(checkpoint_dict) != 0 and train_seq_dataset != None and train_tree_dataset != None and train_rgt_dataset != None


def setup_checkpoints(_):
    global checkpoint_dict

    for model_name in SUPPORTED_MODELS:
        path = get_checkpoint_path(model_name)
        current_app.logger.info(
            f"loading checkpoint {path} for model '{model_name}'...")
        # print(f"[setup_checkpoints] loading checkpoint {path} for model '{model}'...")
        checkpoint_dict[model_name] = torch.load(path)
        # print(f"[setup_checkpoints] checkpoint {path} loaded!")
        current_app.logger.info(f"checkpoint {path} loaded!")

    # print("!!setup_checkpoints finished!!")
    current_app.logger.info("!!setup_checkpoints finished!!")


def setup_models(_):
    # no app_context in this method, current_app not avialable
    global train_seq_dataset
    global train_tree_dataset
    global train_rgt_dataset
    if train_seq_dataset is None:
        # print(f"[setup_models] generating {TRAIN_SEQ_DATASET_KEY}...")
        current_app.logger.info(f"generating {TRAIN_SEQ_DATASET_KEY}...")
        train_seq_dataset = SeqDataset(TRAIN_DATA_FILES, TRAIN_TABLE_FILE_PATH)
        # print(f"[setup_models] {TRAIN_SEQ_DATASET_KEY} generated!")
        current_app.logger.info(f"{TRAIN_SEQ_DATASET_KEY} generated!")

    if train_tree_dataset is None:
        # print(f"[setup_models] generating {TRAIN_TREE_DATASET_KEY}...")
        current_app.logger.info(f"generating {TRAIN_TREE_DATASET_KEY}...")
        train_tree_dataset = TreeDataset(
            TRAIN_DATA_FILES, TRAIN_TABLE_FILE_PATH)
        # print(f"[setup_models] {TRAIN_TREE_DATASET_KEY} generated!")
        current_app.logger.info(f"{TRAIN_TREE_DATASET_KEY} generated!")

    if train_rgt_dataset is None:
        current_app.logger.info(f"generating {TRAIN_RGT_DATASET_KEY}...")
        train_rgt_dataset = RGTDataset(TRAIN_DATA_FILES, TRAIN_TABLE_FILE_PATH)
        current_app.logger.info(f"{TRAIN_RGT_DATASET_KEY} generated")

    # print("!!setup_models finished!!")
    current_app.logger.info("!!setup_models finished!!")


def get_checkpoint_path(model: str) -> str:
    """
    return empty string if model not supported
    """
    if model == MODEL_BILSTM:
        return 'Checkpoints/BiLSTM/spider/bilstm_basic_4.pt'

    if model == MODEL_RELATIVE_TRANSFORMER:
        return 'Checkpoints/RelativeTransformer/spider/rel_basic_4.pt'

    if model == MODEL_TRANSFORMER:
        return 'Checkpoints/Transformer/spider/abs_basic_4.pt'

    if model == MODEL_TREELSTM:
        return 'Checkpoints/TreeLSTM/spider/treelstm_basic_4.pt'

    if model == MODEL_RGT:
        return 'Checkpoints/RGT/spider/rgt_basic_4.pt'

    current_app.logger.error("not supported model %s", model)
    return ''


def get_train_dataset(model: str) -> Dataset:
    if model in [MODEL_RELATIVE_TRANSFORMER, MODEL_TRANSFORMER, MODEL_BILSTM]:
        if train_seq_dataset is None:
            current_app.logger.error("%s is not setup!", TRAIN_SEQ_DATASET_KEY)

        return train_seq_dataset
    elif model == MODEL_TREELSTM:
        if train_tree_dataset is None:
            current_app.logger.error(
                "%s is not setup!", TRAIN_TREE_DATASET_KEY)

        return train_tree_dataset
    elif model == MODEL_RGT:
        if train_rgt_dataset is None:
            current_app.logger.error(f"{TRAIN_RGT_DATASET_KEY} is not setup!")

        return train_rgt_dataset
    else:
        current_app.logger.error("not supported model %s", model)
        return None


def build_dataset(model: str, user_request_data_file: str) -> Dataset:
    test_data_files = [user_request_data_file]

    test_set = None
    if model in [MODEL_RELATIVE_TRANSFORMER, MODEL_TRANSFORMER, MODEL_BILSTM]:
        train_set = get_train_dataset(model)
        test_set = SeqDataset(
            test_data_files, TRAIN_TABLE_FILE_PATH, vocab=train_set.vocab)
    elif model == MODEL_TREELSTM:
        train_set = get_train_dataset(model)
        test_set = TreeDataset(
            test_data_files, TRAIN_TABLE_FILE_PATH, vocab=train_set.vocab)
    elif model == MODEL_RGT:
        train_set = get_train_dataset(model)
        test_set = RGTDataset(test_data_files, TRAIN_TABLE_FILE_PATH,
                              down_vocab=train_set.down_vocab, up_vocab=train_set.up_vocab)
    else:
        current_app.logger.error("not supported model %s", model)

    return test_set


def build_model(model_name: str, args, test_dataset: Dataset) -> torch.nn.Module:
    if args is None or test_dataset is None:
        return None

    if model_name == MODEL_BILSTM:
        vocab = test_dataset.vocab
        return BiLSTM(args.down_embed_dim, vocab.size, args.hid_size,
                      vocab.pad_idx, args.dropout, args.max_oov_num,
                      args.copy)

    if model_name == MODEL_RELATIVE_TRANSFORMER:
        vocab = test_dataset.vocab
        return RelativeTransformer(args.down_embed_dim, vocab.size,
                                   args.down_d_model, args.down_d_ff,
                                   args.down_head_num, args.down_layer_num,
                                   args.hid_size, args.dropout, vocab.pad_idx,
                                   args.down_max_dist, args.max_oov_num,
                                   args.copy, args.rel_share, args.k_v_share)

    if model_name == MODEL_TRANSFORMER:
        vocab = test_dataset.vocab
        return AbsoluteTransformer(args.down_embed_dim,
                                   vocab.size,
                                   args.down_d_model,
                                   args.down_d_ff,
                                   args.down_head_num,
                                   args.down_layer_num,
                                   args.hid_size,
                                   args.dropout,
                                   vocab.pad_idx,
                                   max_oov_num=args.max_oov_num,
                                   copy=args.copy,
                                   pos=args.absolute_pos)

    if model_name == MODEL_TREELSTM:
        vocab = test_dataset.vocab
        return TreeLSTM(args.down_embed_dim, vocab.size, TYPE_NUM,
                        args.hid_size, args.dropout, vocab.pad_idx,
                        args.max_oov_num, args.copy)

    if model_name == MODEL_RGT:
        up_vocab = test_dataset.up_vocab
        down_vocab = test_dataset.down_vocab
        return RGT(args.up_embed_dim, args.down_embed_dim, up_vocab.size,
                   down_vocab.size, UP_TYPE_NUM, DOWN_TYPE_NUM, UP_SCHEMA_NUM,
                   args.up_max_depth, args.down_max_dist, args.up_d_model,
                   args.down_d_model, args.up_d_ff, args.down_d_ff,
                   args.up_head_num, args.down_head_num, args.up_layer_num,
                   args.down_layer_num, args.hid_size, args.dropout,
                   up_vocab.pad_idx, down_vocab.pad_idx, args.max_oov_num,
                   args.copy, args.rel_share, args.k_v_share)

    current_app.logger.error("not supported model %s", model_name)
    return None


def evaluate(model: torch.nn.Module, dataset: Dataset, args, model_name: str) -> Tuple[str, float]:
    if model_name not in SUPPORTED_MODELS:
        return "", 0

    model.eval()
    dataloader = DataLoader(dataset, args.eval_batch_size)
    all_predictions = []

    vocab: Vocabulary = None
    down_vocab: Vocabulary = None
    up_vocab: Vocabulary = None
    if isinstance(dataset, RGTDataset):
        down_vocab = dataset.down_vocab
        up_vocab = dataset.up_vocab
        vocab = dataset.down_vocab
    elif isinstance(dataset, SeqDataset):
        vocab = dataset.vocab
    elif isinstance(dataset, TreeDataset):
        vocab = dataset.vocab

    for batch_data in dataloader:
        preds = []
        if model_name in [MODEL_RELATIVE_TRANSFORMER, MODEL_TRANSFORMER, MODEL_BILSTM]:
            batch, _ = get_seq_batch_data(
                batch_data, vocab.pad_idx, device, vocab.size, vocab.unk_idx, args.down_max_dist)
            nodes, questions, rela_dist, copy_mask, src2trg_map = batch
            if model_name == MODEL_RELATIVE_TRANSFORMER:
                nodes, hidden, mask = model.encode(nodes, rela_dist)
            else:  # MODEL_TRANSFORMER, MODEL_BILSTM
                nodes, hidden, mask = model.encode(nodes)
        elif model_name == MODEL_TREELSTM:
            batch, _ = get_tree_batch_data(batch_data, device)
            nodes, types, node_order, adjacency_list, edge_order, questions, copy_mask, src2trg_map = batch
            nodes, hidden, mask = model.encode(
                nodes, types, node_order, adjacency_list, edge_order)
        elif model_name == MODEL_RGT:
            batch, _ = get_RGT_batch_data(batch_data, up_vocab.pad_idx, down_vocab.pad_idx, 
                device, args.down_max_dist, down_vocab.size, down_vocab.unk_idx)
            up_x, up_type_x, down_x, down_type_x, up_depth, up_schema, down_dist, down_lca, questions, AOA_mask, AOD_mask, copy_mask, src2trg_map = batch
            up_nodes, down_nodes, hidden, up_mask, down_mask = model.encode(
                up_x, up_type_x, down_x, down_type_x, up_depth, up_schema,
                down_dist, down_lca, AOA_mask, AOD_mask)
        else:
            current_app.logger.error("not supported model %s", model_name)
            return "", 0

        inputs = questions[:, 0].view(-1, 1)

        if model_name == MODEL_RGT:
            for _ in range(MAX_DECODE):
                inputs = model.down_nodes_embed(inputs)
                cur_out, hidden = model.decode(inputs, up_nodes, down_nodes,
                                               hidden, up_mask, down_mask,
                                               copy_mask, src2trg_map)
                next_input = cur_out.argmax(dim=-1)
                preds.append(next_input)
                next_input[next_input >= down_vocab.size] = down_vocab.unk_idx
                inputs = next_input
        else:
            for _ in range(MAX_DECODE):
                cur_out, hidden = model.decode(
                    inputs, nodes, hidden, mask, copy_mask, src2trg_map)
                next_input = cur_out.argmax(dim=-1)
                preds.append(next_input)
                next_input[next_input >= vocab.size] = vocab.unk_idx
                inputs = next_input

        preds = torch.cat(preds, dim=1)
        all_predictions += preds.tolist()

    total_score, scores, result_predictions, _ = get_metric(all_predictions, dataset.origin_questions, vocab,
                                                  True, dataset.val_map_list, dataset.idx2tok_map_list)

    prediction = result_predictions[0] if len(result_predictions) > 0 else ""
    score = scores[0] if len(scores) > 0 else 0
    total_score = round(total_score, 4)
    score = round(score, 4)
    current_app.logger.info(f"total_score:'{total_score}' with prediction:'{prediction}'")
    return prediction, score


def run_sql2text(model_name: str, user_input_json_path: str, result: EvaluationResult):
    try:
        if model_name not in checkpoint_dict.keys():
            reason = f"checkpoint for model {model_name} is not loaded yet"
            current_app.logger.error(reason)
            result.failedReason = reason
            return

        checkpoint = checkpoint_dict[model_name]
        checkpoint_args = checkpoint['args']
        # build default args
        checkpoint_args.data = "spider"
        checkpoint_args.eval_batch_size = 1

        test_dataset = build_dataset(model_name, user_input_json_path)
        if test_dataset is None:
            reason = f"build dataset for {model_name} failed"
            current_app.logger.error(reason)
            result.failedReason = reason
            return

        model = build_model(model_name, checkpoint_args, test_dataset)
        if model is None:
            reason = f"build model for {model_name} failed"
            current_app.logger.error(reason)
            result.failedReason = reason
            return

        model.to(device)
        model.load_state_dict(checkpoint['model'])
        current_app.logger.info(
            "%s is ready, start evaluate...", model_name)
        prediction, score = evaluate(
            model, test_dataset, checkpoint_args, model_name)
        result.result = prediction
        result.score = score
        result.success = True

    except Exception as err:
        current_app.logger.error(err)
        current_app.logger.error(traceback.format_exc())
        result.failedReason = str(err)
        return

    return
