# ===== 电商智能客服 Agent v2 —— 生产级 Dockerfile =====
# 基础镜像：Python 3.13 精简版（体积小、启动快）
FROM python:3.13-slim

# 中文编码兜底：避免模型返回中文时在容器内触发 'ascii' codec 错误
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
# 日志实时刷出，不被缓冲（容器里看得到逐行日志）
ENV PYTHONUNBUFFERED=1

# 工作目录
WORKDIR /app

# 第 1 层：先装依赖。requirements.txt 改动频率远低于源码，
# 这样改代码时这层能命中缓存，不用重装包。
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 第 2 层：复制源码（.dockerignore 已排除 .env / __pycache__ / *.db / data/）
COPY . .

# 建数据目录，配合 docker-compose 的 volume 持久化会话与商品库
RUN mkdir -p /app/data

# 🆕 RAG：构建时就把知识库向量索引烘焙进镜像（会下载中文向量模型约90MB，需联网）
# 这样容器启动后 kb_search 直接可用，不用运行时再下模型。
RUN python 构建知识库.py

# 服务端口（与 config.端口 一致）
EXPOSE 8003

# 启动命令：用 uvicorn 拉起 FastAPI 应用
# 注意：CLI 方式不会读 config.端口，必须显式 --port 8003
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
