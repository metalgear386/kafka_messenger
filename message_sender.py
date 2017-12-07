#!/usr/bin/python3
"""This program is the main message sender for kafka.
Author: Jeremy Gillespie
"""
import logging
import os
import sys
import time
import hashlib
import kafka
import strict_rfc3339
import bootstrap_servers as servers


class LOGSENDER(object):
    """This class is used to send messages to a kafka server.
    """
    def __init__(self):
        """Here we create a connection to kafka endpoint brokers. We can give
        a list or just a single IP address here. Load balancing will still
        occur with a single IP address. Edit the bootstrap_servers.py
        file as needed.
        """
        self.msg_count = 1
        connected = False
        while connected != True:
            try:
                self.producer = kafka.KafkaProducer(bootstrap_servers=servers.ips)
                print("Connection established.")
                connected = True
            except kafka.errors.NoBrokersAvailable as nobrokers:
                print(str(nobrokers))
                time.sleep(5)

    def incr_msg_count(self):
        """This method increments the msg_count for the object. This is needed for tracking.
        Returns a string.
        """
        self.msg_count = self.msg_count + 1

    @staticmethod
    def prep_checksum(full_msg):
        """This method creates a md5 checksum of a given string input.
        """
        checksum = hashlib.md5(full_msg.encode('utf-8')).hexdigest()
        checksum = "".join(["checksum=", str(checksum)])
        return checksum

    @staticmethod
    def prep_log_src(log_src_title):
        """Gives a title to the messages that are being sent. Returns a string.
        """
        return "".join(["logSrc=", log_src_title, '~~'])

    @staticmethod
    def prep_transmit_time():
        """Here we use the same timestamp module that is used on the Java side so that the times
        are interchangable between the two langauges. Returns a string.
        """
        rfc_time = strict_rfc3339.timestamp_to_rfc3339_localoffset(time.time())
        transmit_time = "".join(["transmitTime=", str(rfc_time), '~~'])
        return transmit_time

    @staticmethod
    def prep_msg(item):
        """Preps the msg to be sent. Returns a string.
        """
        msg = "".join(["msg=", item, "~~"])
        return msg

    def prep_msg_number(self):
        """Here we prep the message count number for sending by looking at the value that is stored
        in that log objects msg_count variable. Returns a string.
        """
        msg_number = "".join(["msgCount=", str(self.msg_count), "~~"])
        return msg_number

    def send_log(self, msg_list, log_src_title):
        """This method that takes a log, reads a number of lines into
        an array, then transmits the messages in the array through to kafka.
        This method is used to increase performance as bursting is faster than
        reading each file back and forth. Notice that each time this runs the
        array is emptied. We append several snippets to the log before sending,
        for tracking purposes.
        """
        log_src = self.prep_log_src(log_src_title)
        for item in msg_list:
            try:
                if item:
                    msg_number = self.prep_msg_number()
                    transmit_time = self.prep_transmit_time()
                    msg = self.prep_msg(str(item))
                    full_msg = "".join([log_src, msg_number, transmit_time, msg])
                    checksum = self.prep_checksum(full_msg)
                    self.producer.send('Test', "".join([full_msg, checksum]).encode())
                    print(full_msg)
                    self.producer.flush()
                    self.incr_msg_count()
                    #receipts.append(future)
                    #print('events', "".join([log_src, \
                    #msg_number, transmit_time, msg]).encode())
            except (NameError, AttributeError) as exception:
                #LOGGER.warning("Failed to send message: " + item + " Exception-->" + exception)
                print(exception)
        return 0

    @staticmethod
    def send_list_of_logs(SENDER, LOGSRC, list_of_messages):
        """This method sends a list of messages to the previously arranged
        kafka queue.
        """
        for func in [ \
            SENDER.send_log(list_of_messages, LOGSRC), \
            ]:
            try:
                func
            except KeyboardInterrupt:
                LOGGER.info("Exited cleanly with KeyboardInterrupt.")
                sys.exit(0)
            except TypeError as type_error:
                print(type_error)

if __name__ == '__main__':
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
    sys.excepthook = my_handler
    LOGGER = start_logging(BASE)
    SENDER = LOGSENDER()
    LOGSRC = "gman"
    EXAMPLE_MESSAGES = ["1", "2", "3", "4"]
    SENDER.send_list_of_logs(EXAMPLE_MESSAGES)
