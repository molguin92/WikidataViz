#!/usr/bin/env bash
# script for remote deploy. Creates a virtualenv, installs requirements and starts the service
rm -rf /tmp/www_wikidataviz
cd /tmp
tar xzmfv ./wikidataviz.tar.gz
mv /tmp/WikidataViz /tmp/www_wikidataviz
virtualenv --python=python3.5 /tmp/www_wikidataviz/venv
cd /tmp/www_wikidataviz
# cat ./.env
# source ./.env
./venv/bin/pip install -r requirements.txt

if [ -f /tmp/gunicorn.pid ]; then
    kill "$(cat /tmp/gunicorn.pid)"
    rm /tmp/gunicorn.pid
fi
if [ -f /tmp/worker.pid ]; then
    kill "$(cat /tmp/worker.pid)"
    rm /tmp/worker.pid
fi

echo "Starting service"
screen -d -m ./venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wikidataviz.wsgi:app --error-logfile errors.log --pid /tmp/gunicorn.pid
screen -d -m ./venv/bin/rq worker --pid /tmp/worker.pid
