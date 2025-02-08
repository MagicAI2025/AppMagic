FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 运行数据库迁移
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 

# 安装 React 类型声明
RUN cd frontend && npm install @types/react @types/react-dom 