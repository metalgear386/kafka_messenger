#!/usr/bin/python3
"""This file runs in the background serving as a websocket and kafka consumer
creator for each user that connects. This needs to be run in the background for
the application to work.
"""
import asyncio
import websockets
import receiver as rc

async def receive_msgs(websocket, path):
    """This creates a new receiver object that consumes messages from the kafka queue.
    As each message is consumed, we send that message contents to the users' websocket.
    This makes messages appear on their side, that used to be in the queue.
    """
    path = path
    newrc = rc.RECEIVER()
    while True:
        await websocket.send(newrc.check_for_msgs())
        #await asyncio.sleep(1)

START_SERVER = websockets.serve(receive_msgs, port='5678')

asyncio.get_event_loop().run_until_complete(START_SERVER)
asyncio.get_event_loop().run_forever()
