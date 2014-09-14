#!/usr/bin/env python3


import asyncio
import websockets
import json


class ControlWS:
    def __init__(self, callback, event_loop):
        if callback != None:
            self.callback = callback
        self.loop = event_loop
        self.start_server = websockets.serve(self.handler, '*', 1337)
    @asyncio.coroutine
    def handler(self, websocket, path):
        while True:
            message = yield from websocket.recv()
            if message is None:
                break
            try:
                receivedData = json.loads(message)
                self.loop.call_soon_threadsafe(self.callback, receivedData)
                #self.callback(receivedData)
                yield from websocket.send(json.dumps(receivedData))
            except ValueError:
                yield from websocket.send("{} was no JSON".format(message))

    def callback(self, receivedData):
        print(json.dumps(receivedData))
        receivedData["response"] = True
        return True
    def start(self):
        self.loop.run_until_complete(self.start_server)
        self.loop.run_forever()

def startup(callback):
    controlws = ControlWS( callback, asyncio.get_event_loop())
    controlws.start()

if __name__ == "__main__":
    try:
        startup(None) 
    except KeyboardInterrupt:
       print("Goodbye")
