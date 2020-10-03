#!/bin/sh

echo "Waiting for MySQL..."

while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  sleep 0.5
  echo '.'
done

echo "MySQL started"

echo "Server starting..."
echo "at $APP_SERVER_HOST:$APP_SERVER_PORT"

echo "DB migrate"
python3 manager.py db init
python3 manager.py db migrate
python3 manager.py db upgrade

gunicorn -w 4 -b $APP_SERVER_HOST:$APP_SERVER_PORT wsgi:app