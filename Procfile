release: sh -c 'python manage.py flush; python manage.py migrate'
web: gunicorn project_django.wsgi --log-file -