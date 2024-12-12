import socket


import asyncio
import websockets

async def handle_websocket(websocket, path):
    async for message in websocket:
        print(f"Received message from client: {message}")
        # Echo the message back to the client
        await websocket.send(f"Server received: {message}")

start_server = websockets.serve(handle_websocket, 'localhost', 8766)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()