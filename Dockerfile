FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 安装系统依赖（MySQL 客户端库，用于连 MySQL 时使用）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb-dev-compat \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件，利用 Docker 缓存
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn mysqlclient

# 复制后端代码
COPY backend/ .

# 创建静态文件目录
RUN mkdir -p static media

# 暴露端口
EXPOSE 8000

# 复制启动脚本
COPY backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]