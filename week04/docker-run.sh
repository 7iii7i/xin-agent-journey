#!/bin/bash
# 一键 build + run：把散装的 docker build / docker run 命令写进这个脚本
# 用法：在 week04 目录下，Git Bash 里执行  bash docker-run.sh

# ① 设钥匙（把等号右边换成你的真实 key；如果终端已设好环境变量，删掉这行也行）
export DEEPSEEK_API_KEY=sk-你的真实key

# ② 打包镜像（等价于 docker build -t agent-demo .）
docker build -t agent-demo .

# ③ 开容器（等价于 docker run -p 8000:8000 -e DEEPSEEK_API_KEY=... agent-demo）
docker run -p 8000:8000 -e DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY agent-demo

# 验证（另开一个终端执行）：
# curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"3加5等于多少\"}"
