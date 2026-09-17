# ===== 配置层（config.py）Tier 2 =====
# 升级点：
#   ① 用 pydantic-settings 管配置（原来用普通 class + os.environ，Tier 1 就预留了）
#   ② 客户端换成 AsyncOpenAI（异步，配合全链路 async）
#   ③ 加 logging，方便以后排查"为什么某轮调了工具 / 流式断了"
import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from openai import AsyncOpenAI

load_dotenv()  # 读 .env 里的 DEEPSEEK_API_KEY（和 pydantic-settings 双保险）


class 设置(BaseSettings):
    # ⚠️ 必填项：.env 里必须有 DEEPSEEK_API_KEY，否则启动直接报错（比 KeyError 友好）
    DEEPSEEK_API_KEY: str
    BASE_URL: str = "https://api.deepseek.com"
    MODEL: str = "deepseek-chat"
    DB名: str = "shop.db"          # 商品库（和 v1.1 共用，避免重复播种）
    会话DB名: str = "sessions.db"  # 会话库（v2 多轮记忆）
    端口: int = 8003              # 避开 8001 / 8002

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


配置 = 设置()

# 全项目只有一个异步客户端（🔴死记：异步项目里客户端也必须是 AsyncOpenAI）
client = AsyncOpenAI(api_key=配置.DEEPSEEK_API_KEY, base_url=配置.BASE_URL)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
日志 = logging.getLogger("ecommerce_agent")
