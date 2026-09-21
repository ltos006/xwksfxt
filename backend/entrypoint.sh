#!/bin/bash
set -e

# 创建/更新超级管理员
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "检查超级管理员用户..."
    python manage.py shell -c "
from users.models import User
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME', role='admin').exists():
    User.objects.create_superuser(username='$DJANGO_SUPERUSER_USERNAME', password='$DJANGO_SUPERUSER_PASSWORD', phone='13800138000')
    print('已创建管理员用户: $DJANGO_SUPERUSER_USERNAME')
else:
    print('管理员用户已存在，跳过创建')
"
fi

python manage.py migrate --noinput

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 启动 Gunicorn
echo "启动 Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-10000} \
    --workers 2 \
    --access-logfile - \
    --error-logfile -
