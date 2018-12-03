import json
import logging
import requests
import sys

from settings import ES_RANGE_WINDOW, NOTIFICATION_CHANNELS
from settings import SLACK_HOOK, KIBANA, SLACK_CHANNEL, ACTIVATE_ALARM_GOOD
from settings import HOST_URL, PATH_ERROR, PATH_WARN


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
    message = f"""
        {msg}
        Information about errors: {api_logs()}
    """
    payload = {
        "channel": f"#{SLACK_CHANNEL}",
        "username": "webhookbot",
        "icon_emoji": emoji.get(kind),
        "text": message
    }
    res = requests.post(SLACK_HOOK, json=payload)
    if res.status_code == 200:
        logger.info(f"Success Slack notification: type -> `{kind}`")
    else:
        logger.error(f"Fail notification: {res.text}")


def api_logs():
    try:
        rq_errors = requests.get(url=f"{HOST_URL}{PATH_ERROR}")
        # rq_errors.raise_for_status()
        errors = json.dumps(rq_errors.json(), indent=4)
        if not errors:
            rq_warns = requests.get(url=f"{HOST_URL}{PATH_WARN}")
            return json.dumps(rq_warns.json(), indent=4)
        return errors
    except requests.exceptions.RequestException as re:
        logger.error(f"API LOGS FAILED: see trace errors: {re}")


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
                logger.info(f"{msg}: type -> `{kind}`")
        except TypeError:
            logger.error(f"Invalid notification channel: {channel}")
            sys.exit(1)
