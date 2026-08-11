#!/bin/bash
set -e

# 等待数据库就绪（如果使用 MySQL）
if [ "$DB_ENGINE" = "mysql" ]; then
    echo "等待 MySQL 就绪..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 1
    done
    echo "MySQL 已就绪"
fi

# 数据库迁移
echo "执行数据库迁移..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 启动 Gunicorn
echo "启动 Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --access-logfile - \
    --error-logfile -