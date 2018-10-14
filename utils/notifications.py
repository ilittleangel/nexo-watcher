import logging
import sys

from settings import ES_RANGE_WINDOW, NOTIFICATION_CHANNELS


logger = logging.getLogger('watcher')


# todo: implement TWITTER notifications
def twitter(msg):
    logger.debug(f"twitter notification: {msg}")


# todo: implement EMAIL notifications
def email(msg):
    logger.debug(f"email notification: {msg}")


# todo: implement SLACK notifications
def slack(msg):
    logger.debug(f"slack notification: {msg}")


def notify(hits, kind):
    switcher = {
        'bad': f"Something happens: {hits} hits in the las {ES_RANGE_WINDOW} minutes",
        'very bad': f"Something really bad happens: {hits} hits in the las {ES_RANGE_WINDOW} minutes",
        'twitter': twitter,
        'email': email,
        'slack': slack
    }
    msg = switcher.get(kind, "Invalid kind of message")
    for channel in NOTIFICATION_CHANNELS:
        try:
            func = switcher.get(channel)
            func(msg)
        except TypeError:
            logger.error(f"Invalid notification channel: {channel}")
            sys.exit(1)
