from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from wikidataviz import wd
from wikidataviz.models.graphs import deferred_graph_build
from wikidataviz.models.jobs import enqueue_job_and_return


class GraphView(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('id', type=str, required=True)

    def get(self):
        args = self.parser.parse_args()
        id = args['id']

        return enqueue_job_and_return(deferred_graph_build, wd[id])
