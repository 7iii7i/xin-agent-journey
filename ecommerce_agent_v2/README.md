# 电商智能客服 Agent（v2）

一个基于 **FastAPI + LLM 工具调用 + 服务端会话记忆** 的电商客服示例项目，支持**异步高并发**与**流式打字机回复**。可作为「Agent 开发工程师」方向的简历落地项目：业务真实、架构清晰、可一键 Docker 部署。

---

## 一、业务价值

- **真实场景**：二手/电商小店客服，用户问「耳机多少钱」「还有货吗」「推荐个便宜的」，Agent 自动查商品库、查价、查库存后作答，**答完记得上一句**（多轮上下文）。
- **可迁移**：工具层（tools.py）与业务解耦，换成「工厂库存查询」「闲鱼自动上架」只需改工具，核心编排复用。
- **生产级写法**：异步全链路 + SSE 流式 + 工具注册表 + 分层架构 + 容器化部署，对齐工业界标准，而非玩具 demo。

---

## 二、技术栈

| 层 | 技术 |
|---|---|
| Web 框架 | FastAPI（异步 ASGI） |
| 模型 | DeepSeek `deepseek-chat`（OpenAI 兼容协议，AsyncOpenAI 客户端） |
| 数据库 | SQLite（异步 `aiosqlite`）—— 商品库 + 会话库 |
| 流式 | SSE（Server-Sent Events，`StreamingResponse`） |
| 配置 | pydantic-settings + `.env` |
| 部署 | Docker + docker-compose |
| 测试 | pytest + unittest.mock（离线 mock LLM） |

---

## 三、分层架构

```
浏览器(原生 HTML/JS 聊天页)
        │  POST /ask  {session_id, question}
        ▼
┌─────────────────────────────────────────────┐
│ main.py  (接口层 / 入口)                       │
│   - /          返回聊天页                      │
│   - /ask       调 跑_agent，SSE 流式返回        │
│   - /history   取某 session 历史               │
│   - CORS / lifespan(初始化数据库)              │
└───────────────┬───────────────────────────────┘
                │ 跑_agent(历史)
                ▼
┌─────────────────────────────────────────────┐
│ agent.py  (Agent 编排层)                       │
│   while 轮次<上限:                             │
│     ① 非流式判断 → 有无 tool_calls？           │
│     ② 有 → 注册表.调用(工具) → 结果回灌模型     │
│     ③ 无 → 流式 yield 每个 token（打字机）      │
└───────────────┬───────────────────────────────┘
                │ 注册表.调用(name, 参数)
                ▼
┌─────────────────────────────────────────────┐
│ tools.py  (工具注册表)                         │
│   注册表.注册(schema, 函数)  /  注册表.调用()   │
│   工具：search_product / get_price / get_stock │
└───────────────┬───────────────────────────────┘
                │ 真正查数据
                ▼
┌─────────────────────────────────────────────┐
│ db.py  (数据层)                               │
│   商品库：建表/播种/搜商品/查价/查库存           │
│   会话库：建表/追加/取历史（按 session 隔离）   │
└───────────────┬───────────────────────────────┘
                │ 配置
                ▼
┌─────────────────────────────────────────────┐
│ config.py  (配置层)                           │
│   pydantic-settings 管 key/端口/模型；AsyncOpenAI │
└─────────────────────────────────────────────┘
```

**依赖方向单向**：`config ← db ← tools ← agent ← main`，无循环引用，每层职责单一、易测试。

---

## 四、能力清单（Tier 1 → 3）

| 梯级 | 能力 | 状态 |
|---|---|---|
| Tier 1 | 分层架构 / 工具注册表（替代 if-elif）/ 服务端会话记忆（多轮） | ✅ |
| Tier 2 | 全异步（aiosqlite + AsyncOpenAI）/ SSE 流式打字机 / CORS / 配置分层 | ✅ |
| **Tier 3** | **Docker 容器化部署 / 正式 pytest 套件 / 本 README** | ✅ |

---

## 五、目录结构

```
ecommerce_agent_v2/
├── config.py          # 配置层
├── db.py              # 数据层（商品库 + 会话库，异步）
├── tools.py           # 工具注册表
├── agent.py           # Agent 编排（异步生成器，流式）
├── main.py            # 接口层（FastAPI + SSE + CORS）
├── index.html         # 前端聊天页（原生 JS，SSE 读取）
├── requirements.txt   # 依赖
├── Dockerfile         # 容器构建
├── docker-compose.yml # 一键部署
├── .dockerignore      # 排除密钥/缓存/本地库
├── .env               # DEEPSEEK_API_KEY（勿提交真实值到公开仓库）
├── tests/
│   └── test_agent.py  # 离线 pytest（mock LLM）
├── 启动服务.bat        # Windows 一键启动（受管 venv）
├── 异步流式巩固卡.html   # 学习卡片
├── 死记骨架默写卡.html   # 学习卡片
└── data/              # 运行时生成：shop.db / sessions.db（Docker 挂载持久化）
```

---

## 六、本地运行

### 方式一：双击脚本（Windows，最省事）
双击 `启动服务.bat` → 弹窗别关 → 浏览器开 `http://localhost:8003/`

### 方式二：命令行
```bash
cd ecommerce_agent_v2
pip install -r requirements.txt      # 首次
python main.py                       # 保持窗口开着
# 浏览器打开 http://localhost:8003/
```
> ⚠️ `.env` 必须有 `DEEPSEEK_API_KEY=sk-xxxx`，否则启动报错。

---

## 七、Docker 部署（推荐交付方式）

```bash
cd ecommerce_agent_v2
# 1) 确保 .env 里已配置 DEEPSEEK_API_KEY
# 2) 构建并后台启动
docker compose up --build -d
# 3) 浏览器开 http://localhost:8003/
# 查看日志：docker compose logs -f
# 停止：     docker compose down
```
- 会话库与商品库挂载在命名卷 `agent_data`，**容器重建不丢历史**。
- 容器内已设中文编码兜底（PYTHONIOENCODING / LANG / LC_ALL），中文不会乱码。
- 密钥通过 `env_file` 运行时注入，**不打进镜像**（`.dockerignore` 已排除 `.env`）。

---

## 八、测试

不调真实 API、不联网，离线验证核心逻辑：

```bash
cd ecommerce_agent_v2
python -m pytest tests/ -v
```

覆盖：
1. **异步工具注册表分发 + 流式最终轮**：模型经「工具轮非流式 → 最终轮判断 → 流式逐字」拼出完整答案。
2. **异步会话库隔离**：同一 session 历史按序可取，不同 session 互不串。

---

## 九、API 说明

### `POST /ask`
请求：
```json
{ "session_id": "sess_abc123", "question": "耳机多少钱" }
```
响应（SSE 流，逐字）：
```
data: "耳"
data: "机"
data: " Pro 199元"
...
```

### `GET /history?session_id=xxx`
返回该 session 的历史对话列表。

### `GET /`
返回聊天前端页面。

---

## 十、关键设计点（面试可讲）

1. **工具轮非流式、最终轮流式**：流式中的 `tool_calls` 是碎片、需手动拼，易出 bug；故「判断调哪个工具」走干净的非流式，「正式回答」才流式——这是踩坑后的最优解。
2. **参数名必须 == JSON schema 的 key**：注册表用 `func(**参数)` 展开，方法形参名须与工具 schema 的 `properties` key 完全一致，否则 `TypeError`。
3. **服务端会话记忆**：前端生成 `session_id` 存 `localStorage`，后端按 session 存/取历史，实现多用户上下文隔离。
4. **DB 路径收敛到 `data/`**：配合 Docker 挂载卷持久化，且 `初始化()` 里 `os.makedirs` 兜底建目录。
5. **可测性**：LLM 依赖 mock 掉，业务逻辑可离线、稳定测试，无需密钥与网络。
