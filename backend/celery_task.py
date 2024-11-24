from celery import Task
from app import createApp

app, _, _ = createApp()


class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)