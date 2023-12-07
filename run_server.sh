# wait mysql
while ! nc -z $DB_HOST $DB_PORT; do sleep 3; done

# run test
python manage.py test
if [ $? -ne 0 ]; then
    echo "Test failed"
    exit 1
fi

# update database
python manage.py migrate

# run server
python manage.py collectstatic --noinput
gunicorn geonet_api.wsgi:application :$PORT
