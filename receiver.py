#!/usr/bin/python3
"""This file is imported and used to pull messages from kafka.
"""
import json
from kafka import KafkaConsumer

class RECEIVER(object):
    """This is a class that gets created per user session to receive messages
    from kafka.
    """
    def __init__(self):
        """This creates a new consumer and starts comsuming from the latest
        message for a topic
        """
        self.consumer = KafkaConsumer()
        
        #print("Receiver is connected!")

    def check_for_msgs(self):
        """This method pulls each message from the queue, parses it and returns
        JSON in the form of user: message.
        """
        for msg in self.consumer:
            #print(msg)
            message = json.loads(msg.value.decode())
            return ": ".join([message["user"], message["msg"]])



    def get_all_msgs(self):
        """This method gets all messages in the history for a queue. Allows a user
        to see the past messages that happened while they weren't logged in.
        """
        self.consumer = KafkaConsumer(auto_offset_reset="earliest")
        self.consumer.subscribe(['Test'])
        for msg in self.consumer:
            #print(msg)
            message = json.loads(msg.value.decode())
            return ": ".join([message["user"], message["msg"]])

    def subscribe_to_topic(self, topic):
        self.consumer.subscribe([topic])


if __name__ == "__main__":
    RC = RECEIVER()
    RC.subscribe_to_topic("Test")
    while True:
        print(RC.check_for_msgs())
