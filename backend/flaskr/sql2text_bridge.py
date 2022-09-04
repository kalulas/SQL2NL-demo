from flask import current_app
from flaskr import file_utils
from Model.model import RelativeTransformer
from torch.utils.data import Dataset
from Data.dataset import SeqDataset, TreeDataset
import torch

device = torch.device("cuda:0")

def predict(model:str, input_sql:str, input_identifier:str):
    # current_app.logger.info(f"you are on bridge, torch version:{torch.__version__}")
    jsonTargetPath = file_utils.build_input_sql_json(input_sql, input_identifier)
    if jsonTargetPath == "":
        return
    
    run_sql2text(model, jsonTargetPath)
    return f"[{model}] {input_sql}\n"

def get_checkpoint(model:str) -> str:
    """
    return empty string if model not supported
    """
    if model == 'BiLSTM':
        return 'Checkpoints/BiLSTM/spider/bilstm_1.pt'
    
    if model == 'Relative-Transformer':
        return 'Checkpoints/RelativeTransformer/spider/rel_transformer_1.pt'

    if model == 'Transformer':
        return 'Checkpoints/Transformer/spider/transformer_1.pt'

    if model == 'TreeLSTM':
        return 'Checkpoints/TreeLSTM/spider/tree2seq_3.pt'
    
    current_app.logger.error("not supported model %s", model)
    return ''

def build_dataset(model:str, user_input_json_path:str, checkpoint_args) -> Dataset:
    test_dataset = None
    train_table_file_path = "Dataset/spider/tables.json"
    user_input_json_path = [user_input_json_path]
    if model in ['Relative-Transformer', 'Transformer', 'BiLSTM']:
        test_dataset = SeqDataset(user_input_json_path, train_table_file_path, min_freq=checkpoint_args.min_freq)
    elif model == 'TreeLSTM':
        test_dataset = TreeDataset(user_input_json_path, train_table_file_path, min_freq=checkpoint_args.min_freq)
    else:
        current_app.logger.error("not supported model %s", model)
    
    return test_dataset


def run_sql2text(model:str, user_input_json_path:str):
    checkpoint_path = get_checkpoint(model)
    if checkpoint_path == '':
        return
    
    checkpoint_args = torch.load(checkpoint_path)['args']
    # default args
    checkpoint_args.data = "spider"
    checkpoint_args.eval_batch_size = 1
    test_dataset = build_dataset(model, user_input_json_path, checkpoint_args)
    if test_dataset is None:
        return
    
    current_app.logger.info(str(test_dataset))
    print(checkpoint_args.output)

    return checkpoint_path
