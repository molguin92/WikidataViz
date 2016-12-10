from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask_restful import Api
from redis import Redis
from rq import Queue
from itsdangerous import URLSafeSerializer
import os

app = Flask(__name__)
api = Api(app)
app.secret_key = os.environ.get('WIKIDATAVIZ_SECRET_KEY', '1234')
app.config['RESULT_TTL_SECONDS'] = 1800

queue = Queue(connection=Redis())

job_serializer = URLSafeSerializer(app.secret_key, salt='jobs')

from wikidataviz.views.gview import GraphView
from wikidataviz.views.jobs import JobResource

api.add_resource(GraphView, '/entity')
api.add_resource(JobResource, '/job')


@app.route('/')
def helloworld():
    return 'plas'


@app.route('/<string:qid>')
def index(qid):
    return render_template('index.html', data=qid)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == '__main__':
    app.run()
