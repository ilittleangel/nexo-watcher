import logging
import json
import re
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

from settings import ES_NODE, ES_PATTERN, ES_USER, ES_PASS


logger = logging.getLogger('watcher')
date_patter = re.compile(r'(20\d{2})(\d{2})(\d{2})')


def get_newest_index():
    """Returns the last indice of elasticsearch
    for perform a search just in one indice"""

    try:
        rq = requests.get(f"{ES_NODE}/_cat/indices", auth=HTTPBasicAuth(ES_USER, ES_PASS))
        logger.debug(f"Indices found:\n\r{rq.text}")
        rq.raise_for_status()

        indices_with_pattern = [line.split()[2] for line in rq.text.splitlines()
                                if line.split()[2].startswith(ES_PATTERN) and
                                date_patter.match(line.split()[2][-len(ES_PATTERN)+1:])]

        indices = sorted(indices_with_pattern,
                         key=lambda x: datetime.strptime(x[-len(ES_PATTERN)+1:], '%Y%m%d'),
                         reverse=True)

        logger.debug(f"Indices found with pattern '{ES_PATTERN}': {len(indices)}")
        logger.info(f"Last index: {indices[0]}")
        return indices[0]

    except IndexError as ie:
        logger.error(f"Index Not found: {ie}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Something wrong with get_newest_index(): {e}")


def search(index, window):
    url = f"{ES_NODE}/{index}/_search"
    headers = {'Content-type': 'application/json'}
    payload = {
        'query': {
            'range': {
                '@timestamp': {'from': f'now-{window}m', 'to': 'now'}
            }
        }
    }

    try:
        rq = requests.get(url=url, headers=headers, json=payload, auth=HTTPBasicAuth(ES_USER, ES_PASS))
        # rq.raise_for_status()
        if rq.status_code == 200:
            hits = rq.json()['hits']['total']
            logger.debug(f"Elasticsearch _search call total hits: {hits}")
            return hits
        else:
            logger.error(f"Something wrong calling elasticsearch: http_response = {json.dumps(rq.json(), indent=4)}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Something wrong with search(): {e}")
