import requests


def counter(init_val=0, step=1):
    counter_val = init_val
    while True:
        counter_val += step
        yield counter_val


def filter_bad_requests(nodes):
    good_nodes = []
    for node in nodes:
        try:
            if requests.get(node).status_code == 200:
                good_nodes.append(node)
        except requests.exceptions.ConnectionError:
            pass
    return good_nodes
