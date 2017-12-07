#!/usr/bin/python3
"""This is the user interface for sending and receiving messages
Author: Jeremy Gillespie
"""
import receiver as rc
import getpass
import logging
import os
import sys
import message_sender as ms

SENDER = ms.LOGSENDER()
USER = getpass.getuser()

def send_a_msg():
        MESSAGE = [str(input(str(USER + ": ")))]
        SENDER.send_list_of_logs(SENDER, USER, MESSAGE)

while True:
    rc.check_for_msgs()
    send_a_msg()


