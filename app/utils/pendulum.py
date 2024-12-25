import pendulum
from app.core.config import settings

DEFAULT_TIMEZONE = settings.timezone


def now():
    return pendulum.now(DEFAULT_TIMEZONE)


def datetime(year, month, day, hour=0, minute=0, second=0):
    return pendulum.datetime(year, month, day, hour, minute, second, tz=DEFAULT_TIMEZONE)


def parse(date_string, strict=False):
    return pendulum.parse(date_string, tz=DEFAULT_TIMEZONE, strict=strict)


def today():
    return pendulum.today(tz=DEFAULT_TIMEZONE)


def start_of_day():
    return now().start_of('day')


def end_of_day():
    return now().end_of('day')


def difference_in_days(date1, date2):
    return date1.diff(date2).in_days()


def format_date(date, fmt="YYYY-MM-DD HH:mm:ss"):
    return date.format(fmt)
