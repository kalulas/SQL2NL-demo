# SQL2NL 演示项目

为sql2nl项目开发的可交互网页应用，后端基于Flask，前端基于Vue

### 项目结构

```bash
.
│  .gitignore
│  README.md
│
├─backend # 基于Flask的后端
│  ├─flaskr
│  │  │  predict.py # predict接口蓝图
│  │  │  __init__.py # 工厂初始化Flask app
│  │
│  └─instance # 数据库存储（暂未使用）
└─frontend # 基于Vue的前端
    └─sql2nl-demo
        ├─.vscode
        ├─node_modules
        │  ├─vite
        │  └─vue
        ├─public
        └─src
            ├─assets
            └─components
                └─icons
```



### 构建/运行环境要求

#### backend

1. python >= 3.8.12
2. anaconda3 / miniconda3
3. Flask >= 2.1.1
4. PyTorch 1.8.1

```bash
conda create -n [env_name] python=3.8.12
# activate env
pip install Flask==2.1.1
```

#### frontend

node.js(16.17.0 LTS https://nodejs.org/en/download/)

vue@3.2.37(dependencies:vitejs/plugin-vue@^3.0.1, vite@^3.0.4)

项目构建参考

```bash
# ./frontend/
npm init vue@latest
√ Project name: ... sql2nl-demo
√ Add TypeScript? ... No / Yes
√ Add JSX Support? ... No / Yes
√ Add Vue Router for Single Page Application development? ... No / Yes
√ Add Pinia for state management? ... No / Yes
√ Add Vitest for Unit Testing? ... No / Yes
√ Add Cypress for both Unit and End-to-End testing? ... No / Yes
√ Add ESLint for code quality? ... No / Yes
```



### 启动命令

windows下仅支持frontend(vue)项目开发测试，部署需要在linux上执行

#### frontend 开发

```bash
# ./frontend/
  cd sql2nl-demo
  npm install
  npm run dev # 开发测试用，使用日志中提供的ip访问即可
```



#### backend部署

```bash
# Linux only
# 项目根目录执行
$ ./deploy.sh [conda-env-name] [path-to-conda.sh]
```

脚本执行以下操作：

1. 进入vue项目目录进行build
2. 清空flask资源目录
3. 将vue项目build生成目录下的内容拷贝到flask资源目录
4. 切换到指定conda环境下
5. 启动flask服务器



### 参考文档

Flask中文：https://dormousehole.readthedocs.io/en/latest/index.html

Flask快速上手：https://dormousehole.readthedocs.io/en/latest/quickstart.html

Vue官方中文：https://cn.vuejs.org/guide/introduction.html

Vite官方中文：https://cn.vitejs.dev/config/

Python的Web框架Flask + Vue 生成漂亮的词云：https://cloud.tencent.com/developer/article/1592758

使用Flask部署图像分类模型：https://segmentfault.com/a/1190000023319921