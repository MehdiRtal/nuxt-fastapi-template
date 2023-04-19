import time

from worker import app


@app.task
def test():
    time.sleep(5)
    return 'test'