from celery.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import task
from .models import *
from django.conf import settings
from datetime import datetime, timedelta
from buntureviews.celery import app
from data.utils import sink_app_review
import logging

logger = get_task_logger(__name__)
sys_logger = logging.getLogger(__name__)


@periodic_task(
    run_every=(crontab(hour=2, minute=56)), name="sink_reviews", ignore_result=True,
)
def sink_reviews():
    logger.info("Started review sinking")
    try:
        response, message = sink_app_review()
        logger.info(message)
    except:
        logger.info("Internal Error")


# celery -A buntureviews worker -l info
# celery -A buntureviews beat -l info
