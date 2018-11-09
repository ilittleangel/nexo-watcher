import logging
import time

from utils.elastic import get_newest_index, search
from utils.logging import init_logging, close_logging
from utils.notifications import notify
from settings import BASE_DIR, ES_RANGE_WINDOW, SLEEP_MINUTES
from settings import MAX_THRESHOLD, MIN_THRESHOLD


def decide(hits):
    if hits < MIN_THRESHOLD:
        return 'very bad'
    elif hits > MAX_THRESHOLD:
        return 'good'
    else:
        return 'bad'


def main():
    while True:
        indice = get_newest_index()
        hits = search(indice, ES_RANGE_WINDOW)
        notify(hits=hits, kind=decide(hits))
        time.sleep(SLEEP_MINUTES * 60)


if __name__ == '__main__':
    init_logging(f'{BASE_DIR}/logs/watcher')
    logger = logging.getLogger('watcher')
    main()
    close_logging()
