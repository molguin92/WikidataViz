from flask import Flask
from flask import make_response
from flask import render_template
from flask import send_from_directory
from flask_restful import Api
from rdflib import Namespace
from redis import Redis
from rq import Queue
from itsdangerous import URLSafeSerializer
import os
from flask_cache import Cache

wikibase = Namespace('http://wikiba.se/ontology-beta#')
wd = Namespace('http://www.wikidata.org/entity/')
schema = Namespace('http://schema.org/')
wdata = Namespace('https://www.wikidata.org/wiki/Special:EntityData/')

app = Flask(__name__)
api = Api(app)
app.secret_key = os.environ.get('WIKIDATAVIZ_SECRET_KEY', '1234')
app.config['RESULT_TTL_SECONDS'] = 600
app.config['CACHE_CONFIG'] = {'CACHE_TYPE': 'redis',
                              'CACHE_DEFAULT_TIMEOUT': 3600}

cache = Cache(app, config=app.config['CACHE_CONFIG'])

conn = Redis()
queue = Queue(connection=conn)

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
    resp = make_response(send_from_directory('js', path), 200)
    # resp.headers['Cache-Control'] = 'no-cache, must-revalidate'
    return resp
