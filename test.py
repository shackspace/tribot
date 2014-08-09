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
                json.loads(message)
            except ValueError:
                yield from websocket.send("That was no JSON")
        
try:
    controlws = ControlWS()

    start_server = websockets.serve(controlws.handler, 'localhost', 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

except KeyboardInterrupt:
    print("Goodbye")
