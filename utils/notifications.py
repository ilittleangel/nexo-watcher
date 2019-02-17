import logging
import requests
import sys

from settings import ES_RANGE_WINDOW, NOTIFICATION_CHANNELS
from settings import SLACK_HOOK, KIBANA, SLACK_CHANNEL, ACTIVATE_ALARM_GOOD
from settings import HOST, ENDPOINTS, FILE, N_LINES, FILE_WATCHER


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
    message = f"{msg}\nInformation about errors: ```{api_logs(kind)}```"
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


def api_logs(kind):
    try:
        if kind == 'very bad':
            log_error = requests.get(url=f"{HOST}/api/logs/error?file={FILE}&nlines={N_LINES}").json()
            log_warn = requests.get(url=f"{HOST}/api/logs/warning?file={FILE}&nlines={N_LINES}").json()
            log_info = requests.get(url=f"{HOST}/api/logs/info?file={FILE_WATCHER}&nlines={N_LINES}").json()
            return [log_error, log_warn, log_info]
        else:
            return [requests.get(url=f"{HOST}{endpoint}?file={FILE}&nlines={N_LINES}").json()
                    for endpoint in ENDPOINTS]

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
    logger.info(f"{msg}: type -> `{kind}`")
    for channel in NOTIFICATION_CHANNELS:
        try:
            func = switcher.get(channel)
            if kind == "bad" or kind == "very bad" or ACTIVATE_ALARM_GOOD:
                func(msg, kind)
        except TypeError as te:
            logger.error(f"Invalid notification channel: {channel}: {te}")
            sys.exit(1)
