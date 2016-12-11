from flask_restful import Resource, reqparse
from wikidataviz.models.jobs import *


class JobResource(Resource):
    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('id', type=str, required=True)

    def get(self):
        args = self.get_parser.parse_args()
        return check_job(args['id'])
