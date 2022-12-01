import os


broker_url = os.getenv("CELERY_BROKER_URL")
result_backend = os.getenv("CELERY_RESULT_BACKEND")
imports = ("tasks",)
task_routes = {
    'run_crawler': {
        'queue': 'crawler_queue'
    }
}

task_create_missing_queues = True

# Prevent Celery sending hundreds of messages per second
# with different diagnostic and redundant heartbeat messages.
worker_send_task_event = True

# Kill task after 2 hours
# task_time_limit = 7200

# Task will raise exception SoftTimeLimitExceeded 
# after 7200 seconds.
task_soft_time_limit = 7200 

# Task messages will be acknowledged after the task has been executed, 
# not just before (the default behavior).
task_acks_late = True

# A worker takes 10 tasks from queue at a time 
# and will increase the performance.
worker_prefetch_multiplier = 10 

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]