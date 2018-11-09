import configparser
from os.path import dirname, abspath


BASE_DIR = dirname(abspath(__file__))

config = configparser.ConfigParser()
config.read('config.ini')

# elastic
elastic = config['ELASTIC']
ES_NODE = elastic['esnode']
ES_PATTERN = elastic['pattern'].lower()
ES_RANGE_WINDOW = elastic.getint('window_minutes', fallback=5)
ES_USER = ""
ES_PASS = ""
try:
    ES_USER = elastic['user']
    ES_PASS = elastic['pass']
except KeyError:
    pass

# logging
LOG_LEVEL = config['LOGGING']['level']

# watcher
watcher = config['WATCHER']
SLEEP_MINUTES = watcher.getint('sleep_minutes', fallback=60)
NOTIFICATION_CHANNELS = watcher['notification_channels'].replace(' ', '').split(',')
SLACK_HOOK = watcher['slack_web_hook']
SLACK_CHANNEL = watcher['slack_channel']
KIBANA = watcher['kibana']
ACTIVATE_ALARM_GOOD = watcher.getboolean('activate_alarm_good', fallback=False)
MAX_THRESHOLD = watcher.getint('max_threshold', fallback=90)
MIN_THRESHOLD = watcher.getint('min_threshold', fallback=1)
