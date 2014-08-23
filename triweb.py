#!/usr/bin/env python3

import asyncio
import websockets
import json


class ControlWS:
    @asyncio.coroutine
    def handler(self, websocket, path):
        while True:
            message = yield from websocket.recv()
            if message is None:
                break
            try:
                receivedData = json.loads(message)
                receivedData["response"] = False
                if(self.callback is not None):
#                    receivedData["response"]=self.callback(receivedData)
                    self.callback(receivedData)
                yield from websocket.send(json.dumps(receivedData))
            except ValueError:
                yield from websocket.send("{} was no JSON".format(message))
    callback = None


def callback(receivedData):
    print(json.dumps(receivedData))
    receivedData["response"] = True
    return True

def startup(callback):
    controlws = ControlWS()
    controlws.callback = callback
    start_server = websockets.serve(controlws.handler, 'lan.tribot.shack', 1337)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    try:
       startup(callback) 
    except KeyboardInterrupt:
       print("Goodbye")
