#!/usr/bin/python3
import json
from kafka import KafkaConsumer
TEST = KafkaConsumer('Test')

print("Receiver is connected!")
topics = []
topics.append(TEST)

def check_for_msgs():
    for topic in topics:
        for msg in topic:
            print(msg)
            message = json.loads(msg.value.decode())
            return ": ".join([message["user"], message["msg"]])  

if __name__ == "__main__":
    while True:
        print(check_for_msgs())
