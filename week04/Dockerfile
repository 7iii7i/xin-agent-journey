# ===== 第 4 层：Dockerfile —— 把整个服务装进集装箱 =====
# 白话：这张"装箱清单"告诉 Docker 怎么从零盖出一台能跑我们服务的机器

# ① 地基：用官方 Python 3.13 精简版当底座（比完整版小很多）
FROM python:3.13-slim

# ② 进店：在容器里建 /app 目录并设为工作目录（后面所有命令都在这里跑）
WORKDIR /app

# ③ 先搬清单：只把依赖清单拷进来，单独装（利用 Docker 缓存，改代码不用重装包）
COPY requirements.txt .

# ④ 装货：按清单装好 fastapi / uvicorn / openai
# --no-cache-dir = 不留安装缓存，镜像更小
RUN pip install --no-cache-dir -r requirements.txt

# ⑤ 搬代码：把当前目录所有文件拷进容器 /app
COPY . .

# ⑥ 开门：声明容器"监听 8000 端口"（只是声明，真正映射在 docker run -p 时做）
EXPOSE 8000

# ⑦ 开业：容器启动时跑这条命令（注意 host 0.0.0.0，否则容器外访问不到）
CMD ["python", "-m", "uvicorn", "api_service:app", "--host", "0.0.0.0", "--port", "8000"]
