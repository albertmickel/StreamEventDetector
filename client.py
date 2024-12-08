# Dec-08-2024: Add a feature to split the stream to a frame sequence and output to two files: 
#              input.txt and target.txt
import argparse
import asyncio
import websockets
import json
from feature import MFeature


async def listen(url, mfea):
    async with websockets.connect(url) as websocket:
        stream = []
        i = 0
        processLen = 20
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            
            stream.append(str(data))
            i += 1
     
            if i == processLen:
                mfea.split_stream(stream)
                stream.clear()
                i = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A WebSocket client to connect to a specified host and port.")
    parser.add_argument("url", type=str, help="A URL corresponding to the WebSocket server (e.g., ws://127.0.0.1:8000)")


    args = parser.parse_args()

    #
    mfeature = MFeature()

    asyncio.run(listen(args.url, mfeature))
