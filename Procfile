release: sh -c 'python manage.py flush --noinput; python manage.py migrate'
web: gunicorn project_django.wsgi --log-file -