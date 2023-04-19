import time

from worker import app


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10, check_emails, name='add every 10')

@app.task(ignore_result=True)
def check_emails(task_type):
    time.sleep(int(task_type) * 10)
    return True