#!/usr/bin/python3
"""This program is the main message sender for kafka.
Author: Jeremy Gillespie
"""
import sys
import json
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
                self.producer = kafka.KafkaProducer(bootstrap_servers=['35.161.252.11'])
                #print("Sender is connected!")
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
        return str(checksum)

    @staticmethod
    def prep_transmit_time():
        """Here we use the same timestamp module that is used on the Java side so that the times
        are interchangable between the two langauges. Returns a string.
        """
        rfc_time = strict_rfc3339.timestamp_to_rfc3339_localoffset(time.time())
        return str(rfc_time)

    @staticmethod
    def prep_msg(item):
        """Preps the msg to be sent. Returns a string.
        """
        return str(item)

    def prep_msg_number(self):
        """Here we prep the message count number for sending by looking at the value that is stored
        in that log objects msg_count variable. Returns a string.
        """
        return str(self.msg_count)

    def send_log(self, msg_list, user, topic):
        """This method that takes a log, reads a number of lines into
        an array, then transmits the messages in the array through to kafka.
        This method is used to increase performance as bursting is faster than
        reading each file back and forth. Notice that each time this runs the
        array is emptied. We append several snippets to the log before sending,
        for tracking purposes.
        """
        msg_contents = {}
        msg_contents.update({"user": user})
        #print(msg_contents)
        #log_src = self.prep_log_src(log_src_title)
        for item in msg_list:
            try:
                if item:
                    #msg_number = self.prep_msg_number()
                    msg_contents.update({"msg_number": self.prep_msg_number()})
                    #transmit_time = self.prep_transmit_time()
                    msg_contents.update({"transmit_time": self.prep_transmit_time()})
                    #msg = self.prep_msg(str(item))
                    msg_contents.update({"msg": self.prep_msg(str(item))})
                    #full_msg = "".join([log_src, msg_number, transmit_time, msg])
                    #checksum = self.prep_checksum(full_msg)
                    #self.producer.send('Test', "".join([full_msg, checksum]).encode())
                    self.producer.send(topic, json.dumps(msg_contents).encode())
                    #print(full_msg)
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
    def send_list_of_logs(sender, user, list_of_messages, topic):
        """This method sends a list of messages to the previously arranged
        kafka queue.
        """
        for func in [ \
            sender.send_log(list_of_messages, user, topic), \
            ]:
            try:
                func
            except KeyboardInterrupt:
                #LOGGER.info("Exited cleanly with KeyboardInterrupt.")
                sys.exit(0)
            except TypeError as type_error:
                print(type_error)
