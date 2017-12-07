#!/usr/bin/python3
import json
from kafka import KafkaConsumer
TEST = KafkaConsumer('Tacos')

print("Receiver is connected!")
topics = []
topics.append(TEST)

def check_for_msgs():
    for topic in topics:
        for msg in topic:
            print(msg)
            message = json.loads(msg.value.decode())
            print(": ".join([message["user"], message["msg"]]))
            break
        break    

if __name__ == "__main__":
    while True:
        check_for_msgs() 

                

