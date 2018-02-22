# kafka_messenger
A great idea to use kafka as a messaging service. 
![alt text](demo_windows.png)

Clone this repo, have docker installed, go to directory, run start_chat_and_server.sh
That should be all you need to start chatting on the local server. For other people to communicate with you will take additional effort in changing the python code but I'm working on making that more accessible.

Todo:
Find a way to stop spamming, or possibly just ingest messages faster. Right not we consume too slowly to handle a large amount of spam, but of course you could just change topic.

List the currently subscribed to topics. It would be nice to see what all topics I am subscribed to.

Direct messaging. This need some heavy design considerations. Since the consumer is fairly anonymous to the system overall, this is somewhat difficult but I'm sure it's possible. Maybe create a uuid per consumer, post it in the dialog, and have it make a topic and auto subscribe. Something like that.

