from .installed_apps import *
from .locale import *
from .settings import *
from .celery import app as celery_app


__all__ = ("celery_app",)
