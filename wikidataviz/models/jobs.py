from datetime import datetime, timezone

import redis
from flask_restful import abort
from itsdangerous import BadSignature

from wikidataviz import job_serializer, app, queue


def enqueue_job_and_return(function, *args):
    try:
        job = queue.enqueue(function, *args,
                            result_ttl=app.config['RESULT_TTL_SECONDS'],
                            timeout=600)
        return {
                   'job': job_serializer.dumps(job.id),
                   'submitted': datetime.now(timezone.utc).isoformat()
               }, 202

    except redis.exceptions.ConnectionError:
        abort(500)


def check_job(job_id):
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
                   'error': True,
                   'result': None
               }, 500

    elif not job.result:
        return {
                   'done': False,
                   'error': False,
                   'result': None
               }, 202
    else:
        return {
                   'done': True,
                   'error': False,
                   'result': job.result
               }, 200
