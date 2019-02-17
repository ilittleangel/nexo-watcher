import logging
import os
import unittest
import sys
from utils.processes import reborn_process


def init_logging():
    logger = logging.getLogger("watcher")
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout)
    logger.addHandler(sh)
    return logger


class FunctionsTest(unittest.TestCase):
    def test(self):
        command = 'python resources/test.py 3'
        os.system(command)
        reborn_process('test.py', command, init_logging())
