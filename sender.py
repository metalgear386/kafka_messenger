#!/usr/bin/python3
"""This program is used to send messages via command line input from the user.
Author: Jeremy Gillespie
"""
import getpass
import logging
import os
import sys
import message_sender as ms

def my_handler(exc_type, value, traceback_call):
    """This method defines how exceptions will be written to log if they are
    not caught exceptions.
    """
    print(str(exc_type))
    print(traceback_call)
    LOGGER.exception("Uncaught exception:" + str(value) + str(exc_type))

def start_logging(file_name):
    """Starts logging on the machine, using the file name as the preface
    to the log's name. We also check to see if the correct folder exists and
    output error messages if it doesnt exist or doesnt have permission correctly.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(file_name + ".log", mode='a')
    handler.setLevel(logging.INFO)
    formatting = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatting)
    logger.addHandler(handler)
    return logger

BASE = os.path.basename(__file__)
LOGGER = start_logging(BASE)
#sys.excepthook = my_handler
LOGGER = start_logging(BASE)
SENDER = ms.LOGSENDER()
#USER = getpass.getuser()
USER = "Jim"
while True:
#def send_a_msg():
        MESSAGE = [str(input(str(USER + ": ")))]
        SENDER.send_list_of_logs(SENDER, USER, MESSAGE)