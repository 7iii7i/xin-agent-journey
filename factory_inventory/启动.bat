@echo off
chcp 65001 >nul
cd /d "%~dp0"

REM 朋友厂一键启动：自动建虚拟环境、装依赖、跑服务
REM 前提：电脑已装 Python 3.11（没装去 python.org 下载安装，勾选"Add to PATH"）

IF NOT EXIST venv (
    echo 正在创建虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate.bat

echo 正在安装依赖...
pip install -r requirements.txt

echo 启动服务中，浏览器打开 http://localhost:8002
python main.py
pause
