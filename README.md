# SQL2NL 演示项目

### 项目结构

```
.
├─backend # 基于Flask的后端
│  ├─flaskr
│  ├─instance
└─frontend # 基于Vue的前端
```

### 构建/运行环境要求

#### backend

python >= 3.8.12

Flask >= 2.1.1

PyTorch 1.8.1

#### frontend

// TODO ...

### 启动命令

#### backend

```bash
# Linux(bash)
# ./backend/
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run --host=0.0.0.0

# windows(cmd)
# ./backend/
> set FLASK_APP=flaskr
> set FLASK_ENV=development
> flask run --host=0.0.0.0
```

### 参考文档

Flask中文：https://dormousehole.readthedocs.io/en/latest/index.html

Flask快速上手：https://dormousehole.readthedocs.io/en/latest/quickstart.html

Vue官方中文：https://cn.vuejs.org/guide/introduction.html

Python的Web框架Flask + Vue 生成漂亮的词云：https://cloud.tencent.com/developer/article/1592758

使用Flask部署图像分类模型：https://segmentfault.com/a/1190000023319921