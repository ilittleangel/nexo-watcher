import os
import time

from utils.elastic import get_newest_index, search
from utils.logging import init_logging, close_logging
from utils.notifications import notify
from utils.processes import reborn_process
from settings import BASE_DIR, ES_RANGE_WINDOW, SLEEP_MINUTES
from settings import MAX_THRESHOLD, MIN_THRESHOLD
from settings import PROCESS_TO_REBORN, PROCESS_COMMAND


def decide(hits):
    if hits < MIN_THRESHOLD:
        return 'very bad'
    elif hits > MAX_THRESHOLD:
        return 'good'
    else:
        return 'bad'


def main():
    import setproctitle
    setproctitle.setproctitle('watcher.py')
    while True:
        indice = get_newest_index()
        hits = search(indice, ES_RANGE_WINDOW)
        current_condition = decide(hits)
        if current_condition == 'very bad':
            reborn_process(PROCESS_TO_REBORN, os.path.expandvars(PROCESS_COMMAND))
        notify(hits=hits, kind=current_condition)
        time.sleep(SLEEP_MINUTES * 60)


if __name__ == '__main__':
    init_logging(f'{BASE_DIR}/logs/watcher')
    main()
    close_logging()
