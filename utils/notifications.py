import logging
import requests
import sys

from settings import ES_RANGE_WINDOW, NOTIFICATION_CHANNELS
from settings import SLACK_HOOK, KIBANA, SLACK_CHANNEL, ACTIVATE_ALARM_GOOD


logger = logging.getLogger('watcher')


# todo: implement TWITTER notifications
def twitter(msg):
    logger.debug(f"twitter notification: {msg}")


# todo: implement EMAIL notifications
def email(msg):
    logger.debug(f"email notification: {msg}")


def slack(msg, kind):
    emoji = {
        'bad': ":fearful:",
        'very bad': ":scream:",
        'good': ":grin:",
    }
    payload = {
        "channel": f"#{SLACK_CHANNEL}",
        "username": "webhookbot",
        "icon_emoji": emoji.get(kind),
        "text": msg
    }
    res = requests.post(SLACK_HOOK, json=payload)
    if res.status_code == 200:
        logger.info(f"Success Slack notification: type -> `{kind}`")
    else:
        logger.error(f"Fail notification: {res.text}")


def notify(hits, kind):
    switcher = {
        'bad': f"Something happens: {hits} hits in the last {ES_RANGE_WINDOW} minutes: <{KIBANA}|click here> for details!",
        'very bad': f"Something really bad happens: {hits} hits in the last {ES_RANGE_WINDOW} minutes: <{KIBANA}|click here> for details!",
        'good': f"Everything is OK: {hits} hits in the last {ES_RANGE_WINDOW} minutes: <{KIBANA}|click here> for details!",
        'twitter': twitter,
        'email': email,
        'slack': slack
    }
    msg = switcher.get(kind, "Invalid type of message")
    for channel in NOTIFICATION_CHANNELS:
        try:
            func = switcher.get(channel)
            if kind == "bad" or kind == "very bad" or ACTIVATE_ALARM_GOOD:
                func(msg, kind)
            else:
                print(f"{msg} | {kind}")
                pass
        except TypeError:
            logger.error(f"Invalid notification channel: {channel}")
            sys.exit(1)
