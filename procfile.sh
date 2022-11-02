# EMERGENCY ONLY!
# Jika deployment tidak berhasil karena tidak bisa migrate, uncomment bagian di bawah.
# python manage.py flush --noinput
# python manage.py migrate
# python manage.py flush --noinput
# python manage.py migrate

python manage.py migrate blog 0004_alter_comment_options_alter_post_options
python manage.py migrate crewdashboard 0004_rename_locations_location
python manage.py migrate
