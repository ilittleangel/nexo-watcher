import configparser
from os.path import dirname, abspath


BASE_DIR = dirname(abspath(__file__))

config = configparser.ConfigParser()
config.read('config.ini')

# elastic
ES_NODE = config['ELASTIC']['esnode']
ES_PATTERN = config['ELASTIC']['pattern'].lower()
ES_RANGE_WINDOW = int(config['ELASTIC']['window_minutes'])
ES_USER = ""
ES_PASS = ""
try:
    ES_USER = config['ELASTIC']['user']
    ES_PASS = config['ELASTIC']['pass']
except KeyError:
    pass

# logging
LOG_LEVEL = config['LOGGING']['level']

# watcher
SLEEP_MINUTES = int(config['WATCHER']['sleep_minutes'])
NOTIFICATION_CHANNELS = config['WATCHER']['notification_channels'].replace(' ', '').split(',')
