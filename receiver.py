#!/usr/bin/python3
import json
from kafka import KafkaConsumer

class RECEIVER(object):
    def __init__(self):
        self.consumer = KafkaConsumer()#, auto_offset_reset="earliest")
        self.consumer.subscribe(['Test'])
        #print("Receiver is connected!")

    def check_for_msgs(self):
        for msg in self.consumer:
                #print(msg)
                message = json.loads(msg.value.decode())
                return ": ".join([message["user"], message["msg"]])  

if __name__ == "__main__":
    rc = RECEIVER()
    while True:
        print(rc.check_for_msgs())
