# 工厂库存查询 Agent —— 部署镜像
# 构建：docker build -t factory-inventory .
# 运行：docker run -d -p 8002:8002 --name fi factory-inventory
FROM python:3.11-slim

WORKDIR /app

# 先装依赖（利用 Docker 层缓存，改代码不必重装包）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再拷贝源码（含 .env，里面是 DeepSeek key；生产环境建议改用环境变量/密钥管理）
COPY . .

EXPOSE 8002

CMD ["python", "main.py"]
