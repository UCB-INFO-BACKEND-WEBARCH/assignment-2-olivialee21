from redis import Redis
from rq import Worker, Queue
import os
from app import create_app

app = create_app()


with app.app_context():
    redis_client = Redis.from_url(os.getenv('REDIS_URL', 'redis://redis:6379'))
    notif_queue = Queue(connection=redis_client)
    worker = Worker([notif_queue], connection=redis_client)
    worker.work()