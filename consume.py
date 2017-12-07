#!/usr/bin/python3
from kafka import KafkaConsumer
Test = KafkaConsumer('Test')
   
print("Connected...")
topics = []
topics.append(Test)
while True:
    for topic in topics:
        for msg in topic:
            print(msg)
