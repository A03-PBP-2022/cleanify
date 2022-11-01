release: sh -c 'python manage.py migrate'
# Jika tidak bisa migrate, ganti release: menjadi ini.
# release: sh -c 'python manage.py migrate; python manage.py flush --noinput; python manage.py migrate'
web: gunicorn project_django.wsgi --log-file -