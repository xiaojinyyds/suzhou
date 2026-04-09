# 苏州石像打卡网站 - 后端 API

基于 **Python + FastAPI + MySQL + Redis + 阿里云OSS** 构建的后端服务。

## 📋 项目信息

- **项目名称**: 苏州石像打卡网站后端 API
- **技术栈**: FastAPI + MySQL + Redis + 阿里云OSS
- **Python 版本**: 3.10+
- **API 文档**: `/docs` (Swagger) / `/redoc` (ReDoc)

## 🚀 快速开始

### 1. 环境准备

确保已安装以下软件：
- Python 3.10+
- MySQL 8.0+
- Redis 6.0+

### 2. 克隆项目

```bash
cd backend
```

### 3. 创建虚拟环境

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入实际的配置信息：
- 数据库连接信息
- Redis 连接信息
- 阿里云 OSS 配置（AccessKey、Bucket等）
- JWT 密钥

### 6. 初始化数据库

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE suzhou_checkin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 初始化数据
python scripts/init_data.py
```

### 7. 启动服务

```bash
# 开发环境（热重载）
python run.py

# 或使用 uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

服务启动后访问：
- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 📁 项目结构

```
backend/
├── app/
│   ├── api/              # API 路由
│   │   └── v1/          # v1 版本 API
│   │       ├── auth.py      # 认证相关
│   │       ├── statues.py   # 石像景点
│   │       ├── checkins.py  # 打卡记录
│   │       ├── desserts.py  # 甜品
│   │       ├── orders.py    # 订单
│   │       └── upload.py    # 文件上传
│   ├── core/            # 核心配置
│   │   ├── config.py        # 配置管理
│   │   ├── database.py      # 数据库连接
│   │   ├── redis_client.py  # Redis 客户端
│   │   └── oss_client.py    # OSS 客户端
│   ├── models/          # 数据模型
│   │   ├── user.py          # 用户模型
│   │   ├── statue.py        # 石像模型
│   │   ├── checkin.py       # 打卡记录
│   │   ├── dessert.py       # 甜品模型
│   │   ├── order.py         # 订单模型
│   │   └── photo.py         # 照片模型
│   ├── schemas/         # Pydantic Schemas
│   │   ├── user.py          # 用户 Schema
│   │   ├── statue.py        # 石像 Schema
│   │   ├── checkin.py       # 打卡 Schema
│   │   ├── dessert.py       # 甜品 Schema
│   │   ├── order.py         # 订单 Schema
│   │   └── common.py        # 通用 Schema
│   ├── utils/           # 工具函数
│   │   ├── distance.py      # 距离计算
│   │   ├── security.py      # 安全工具
│   │   ├── file_helper.py   # 文件处理
│   │   └── order_helper.py  # 订单工具
│   └── main.py          # FastAPI 主应用
├── scripts/
│   └── init_data.py     # 数据初始化脚本
├── .env.example         # 环境变量示例
├── .gitignore           # Git 忽略文件
├── requirements.txt     # Python 依赖
├── run.py              # 启动脚本
└── README.md           # 本文档
```

## 🔌 API 接口

### 认证模块 (`/api/v1/auth`)
- `POST /register` - 用户注册
- `POST /login` - 用户登录
- `POST /refresh` - 刷新 Token
- `GET /me` - 获取当前用户信息

### 石像景点模块 (`/api/v1/statues`)
- `GET /statues` - 获取石像列表
- `GET /statues/{id}` - 获取石像详情
- `GET /statues/nearby` - 获取附近的石像

### 打卡模块 (`/api/v1/checkins`)
- `POST /checkins` - 打卡
- `GET /checkins/my` - 获取我的打卡记录
- `GET /checkins/statistics` - 获取打卡统计

### 甜品模块 (`/api/v1/desserts`)
- `GET /desserts` - 获取甜品列表
- `GET /desserts/{id}` - 获取甜品详情

### 订单模块 (`/api/v1/orders`)
- `POST /orders` - 创建订单
- `GET /orders/my` - 获取我的订单
- `GET /orders/{id}` - 获取订单详情
- `POST /orders/{id}/pay` - 支付订单
- `POST /orders/{id}/cancel` - 取消订单

### 文件上传模块 (`/api/v1/upload`)
- `POST /upload/photo` - 上传照片
- `POST /upload/avatar` - 上传头像

## 🛠️ 开发指南

### 添加新的 API 接口

1. 在 `app/models/` 中定义数据模型（如需要）
2. 在 `app/schemas/` 中定义 Pydantic Schema
3. 在 `app/api/v1/` 中创建路由文件
4. 在 `app/main.py` 中注册路由

### 数据库迁移

使用 Alembic 进行数据库迁移：

```bash
# 生成迁移文件
alembic revision --autogenerate -m "描述信息"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

### 测试

```bash
# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app tests/
```

## 📊 数据库表结构

### 核心表
- `users` - 用户表
- `statues` - 石像景点表
- `check_ins` - 打卡记录表
- `desserts` - 甜品表
- `orders` - 订单表
- `order_items` - 订单明细表
- `photos` - 照片记录表

## 🔒 安全性

- 密码使用 bcrypt 加密存储
- JWT Token 认证机制
- CORS 跨域配置
- 文件上传类型和大小限制
- SQL 注入防护（使用 ORM）

## 🚀 部署

### Docker 部署（推荐）

```bash
# 构建镜像
docker build -t suzhou-checkin-api .

# 运行容器
docker run -d -p 8000:8000 --name suzhou-api suzhou-checkin-api
```

### 传统部署

使用 Gunicorn + Nginx：

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动应用
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 📝 开发日志

- v1.0.0 (2024-11-16)
  - ✅ 初始化项目结构
  - ✅ 配置数据库、Redis、OSS 连接
  - ✅ 创建数据模型
  - ✅ 创建 API 接口骨架
  - ✅ 实现工具函数
  - ⏳ 待实现：业务逻辑、认证中间件、单元测试

## 📞 联系方式

如有问题请联系开发团队。

## 📄 许可证

MIT License
