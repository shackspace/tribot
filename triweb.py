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
                self.callback(receivedData)
                yield from websocket.send(json.dumps(receivedData))
            except ValueError:
                yield from websocket.send("{} was no JSON".format(message))

    def callback(self, receivedData):
        print(json.dumps(receivedData))
        receivedData["response"] = True
        return True

try:
    controlws = ControlWS()
    start_server = websockets.serve(controlws.handler, 'localhost', 1337)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

except KeyboardInterrupt:
    print("Goodbye")
