# ocr_api_server

使用 ddddocr 的最简 api 搭建项目，支持 docker

**建议 python 版本 3.7-3.9 64 位**

# 运行方式

## 最简单运行方式

```shell
# 安装依赖
pip install -r requirements.txt -i https://pypi.douban.com/simple

# 运行  可选参数如下
# --port 8124 指定端口,默认为8124
# --ocr 开启ocr模块 默认开启
# --old 只有ocr模块开启的情况下生效 默认不开启
# --det 开启目标检测模式

# 运行
python main.py --port 8124
```

## docker 运行方式(目测只能在 Linux 下部署)

```shell
# 编译镜像
docker build -t ocr_server:v1 .

# 运行镜像
docker run -p 8124:8124 -d ocr_server:v1

```
