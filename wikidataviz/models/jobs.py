from datetime import datetime, timezone

import redis
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from itsdangerous import BadSignature

from wikidataviz import job_serializer, app, queue


class DeferredResource(Resource):
    """
    Base Resource for deferred results resources.
    """

    def __init__(self):
        self.post_parser = RequestParser()
        self.get_parser = RequestParser()

        self.result_ttl = app.config['RESULT_TTL_SECONDS']

    def enqueue_job_and_return(self, function, *args):
        try:
            job = queue.enqueue(function, *args, result_ttl=self.result_ttl)
            return {
                       'job': job_serializer.dumps(job.id),
                       'submitted': datetime.now(timezone.utc).isoformat()
                   }, 202

        except redis.exceptions.ConnectionError:
            abort(500)

    def check_job(self, job_id):
        try:
            job_id = job_serializer.loads(job_id)
        except BadSignature:
            abort(400, message='Invalid job id')

        job = queue.fetch_job(job_id)
        if not job:
            abort(404, message='No such job, or job discarded on TTL timeout.')

        if job.exc_info:
            # error
            return {
                       'done': True,
                       'result': {
                           'message': (job.exc_info.data.get('message','Unknown Error') if hasattr(job.exc_info, 'data') else 'Unknown Error')
                       },
                       'length': -1,
                       'result_ttl': 0,
                       'timestamp': datetime.now().isoformat(),
                   }, 400

        elif not job.result:
            return {
                       'done': False,
                       'result': None,
                       'length': 0,
                       'result_ttl': self.result_ttl,
                       'timestamp': None
                   }, 202
        else:
            result = job.result if type(job.result) == list else [job.result]
            return {
                       'done': True,
                       'result': result,
                       'length': len(result),
                       'result_ttl': self.result_ttl,
                       'timestamp': job.ended_at.isoformat()
                   }, 200
