from datetime import datetime

from pytz import timezone

from controller.config import Config


def now():
    return datetime.now(tz=timezone(Config.TIMEZONE))
