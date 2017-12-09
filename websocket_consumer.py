#!/usr/bin/python3
import asyncio
import datetime
import random
import websockets
import receiver as rc

async def receive_msgs(websocket, path):
    newrc = rc.RECEIVER()
    while True:
        await websocket.send(newrc.check_for_msgs())
        #await asyncio.sleep(1)

start_server = websockets.serve(receive_msgs, port='5678')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()