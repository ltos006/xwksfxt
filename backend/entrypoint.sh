#!/bin/bash
set -e

# 确保数据目录存在（SQLite 数据库文件需要）
mkdir -p /var/data

# 先执行数据库迁移，确保表存在
python manage.py migrate --noinput

# 创建/更新超级管理员（必须在 migrate 之后，否则 users 表不存在）
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "检查超级管理员用户..."
    python manage.py shell -c "
from users.models import User
user, created = User.objects.update_or_create(
    username='$DJANGO_SUPERUSER_USERNAME',
    role='admin',
    defaults={
        'is_staff': True,
        'is_superuser': True,
        'phone': '13800138000',
    }
)
if created:
    user.set_password('$DJANGO_SUPERUSER_PASSWORD')
    user.save()
    print('已创建管理员用户: $DJANGO_SUPERUSER_USERNAME')
else:
    user.set_password('$DJANGO_SUPERUSER_PASSWORD')
    user.save()
    print('管理员用户已存在，密码已更新: $DJANGO_SUPERUSER_USERNAME')
"
fi

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
