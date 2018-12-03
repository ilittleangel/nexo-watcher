import configparser
from os.path import dirname, abspath


BASE_DIR = dirname(abspath(__file__))

config = configparser.ConfigParser()
config.read('config.ini')

# elastic
elastic_cfg = config['ELASTIC']
ES_NODE = elastic_cfg['esnode']
ES_PATTERN = elastic_cfg['pattern'].lower()
ES_RANGE_WINDOW = elastic_cfg.getint('window_minutes', fallback=5)
ES_USER = ""
ES_PASS = ""
try:
    ES_USER = elastic_cfg['user']
    ES_PASS = elastic_cfg['pass']
except KeyError:
    pass

# logging
LOG_LEVEL = config['LOGGING']['level']

# watcher
watcher_cfg = config['WATCHER']
SLEEP_MINUTES = watcher_cfg.getint('sleep_minutes', fallback=60)
NOTIFICATION_CHANNELS = watcher_cfg['notification_channels'].replace(' ', '').split(',')
SLACK_HOOK = watcher_cfg['slack_web_hook']
SLACK_CHANNEL = watcher_cfg['slack_channel']
KIBANA = watcher_cfg['kibana']
ACTIVATE_ALARM_GOOD = watcher_cfg.getboolean('activate_alarm_good', fallback=False)
MAX_THRESHOLD = watcher_cfg.getint('max_threshold', fallback=90)
MIN_THRESHOLD = watcher_cfg.getint('min_threshold', fallback=1)

# api logs
api_cfg = config['API_LOGS']
HOST_URL = api_cfg['host_url']
PATH_ERROR = api_cfg['full_path_error']
PATH_WARN = api_cfg['full_path_warning']
