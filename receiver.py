#!/usr/bin/python3
"""This file is imported and used to pull messages from kafka.
"""
import json
import time
from kafka import KafkaConsumer

class RECEIVER(object):
    """This is a class that gets created per user session to receive messages
    from kafka.
    """
    def __init__(self):
        """This creates a new consumer and starts comsuming from the latest
        message for a topic
        """
        print("Connecting...")
        self.consumer = KafkaConsumer(bootstrap_servers=['35.161.252.11'], request_timeout_ms = 10000, session_timeout_ms = 5000, heartbeat_interval_ms = 4000)
        self.topics_subbed = []

    def check_for_msgs(self):
        """This method pulls each message from the queue, parses it and returns
        a list of JSON in the form of user: message.
        """ 
        data = self.consumer.poll()
        if data != {}:
            message = []
            for i in data.values():
                for x in i:
                    topic = x.topic 
                    for f in x:
                        try:
                            temp_msg = json.loads(f.decode())
                            #print(temp_msg.keys())
                            user = temp_msg["user"]
                            msg = temp_msg["msg"]
                            message.append("--".join([topic, user, msg ]))
                        except:
                            pass
            return message

    def subscribe_to_topic(self, topic):
        self.topics_subbed.append(topic)
        self.consumer.subscribe(self.topics_subbed)

    def unsubscribe_from_topic(self, topic):
        self.topics_subbed.remove(topic)
        self.consumer.unsubscribe()
        self.consumer.subscribe(self.topics_subbed)

if __name__ == "__main__":
    RC = RECEIVER()
    RC.subscribe_to_topic("Test")
    while True:
        print(RC.check_for_msgs())
