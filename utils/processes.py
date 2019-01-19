import logging
import psutil
import os
import sys


def _kill(name, logger):
    for process in psutil.process_iter():
        try:
            if name in [proc for proc in process.cmdline()]:
                logger.info(f"Process {name} found: {process}")
                logger.info(f"killing {name} ...")
                process.terminate()
                break
        except psutil.Error:
            pass
    else:
        logger.info(f"Process not found.")


def _run(name, command, logger):
    logger.info(f"Starting {name} ...")
    logger.info(f"command: {command}")
    try:
        # status = subprocess.run(command.split(' ')).returncode
        status = os.system(command)
        if status == 0:
            logger.info(f"{name} started!")
        else:
            logger.error(f"{name} was not started: returncode -> {status}")
    except OSError as oe:
        logger.error("Execution failed:", oe, file=sys.stderr)
        sys.exit(1)


def reborn_process(name, command, logger=logging.getLogger('watcher')):
    logger.info(f"Reborn {name}...")
    _kill(name, logger)
    _run(name, command, logger)
