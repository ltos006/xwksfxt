# ---------- 阶段1：构建前端 ----------
FROM node:18-alpine AS frontend-build
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build            # 产物在 /app/dist

# ---------- 阶段2：后端运行时 ----------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 安装系统依赖（保留 gcc 以防 mysqlclient；仅 SQLite 时也无害）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb-dev-compat \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件，利用 Docker 缓存
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn whitenoise

# 复制后端代码
COPY backend/ .

# 创建静态/媒体目录
RUN mkdir -p static media

# 把前端构建产物拷进 Django 静态目录，collectstatic 时一并收纳
COPY --from=frontend-build /app/dist ./static/frontend

# 暴露 Render 默认端口
EXPOSE 10000

# 复制启动脚本（去 CRLF，保证 Linux 下 shebang 生效）
COPY backend/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
