# wait mysql
while ! nc -z $DB_HOST $DB_PORT; do sleep 3; done

# update database
python manage.py migrate

# run server
python manage.py collectstatic --noinput
gunicorn geonet_api.wsgi:application :$PORT
