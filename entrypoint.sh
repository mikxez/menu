#!/bin/sh

python manage.py migrate --noinput

python manage.py collectstatic --noinput

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="$SUPER_USER_NAME").exists():
    User.objects.create_superuser("$SUPER_USER_NAME", "$SUPER_USER_EMAIL", "$SUPER_USER_PASSWORD")
EOF

gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
