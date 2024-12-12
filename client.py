import socket

'''
# AF_INET = IPv4, SOCK_STREAM = TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))  # Connect to the server

while True:
    msg = s.recv(1024)
    print(msg.decode("utf-8"))

'''
'''
import asyncio
import websockets

async def send_message(message):
    try:
        async with websockets.connect('ws://localhost:8765') as websocket:
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Received response: {response}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed with code {e.code}: {e.reason}")

# Connect to the WebSocket server and send messages
asyncio.get_event_loop().run_until_complete(send_message('restart_server'))
asyncio.get_event_loop().run_until_complete(send_message('read_logs'))

###########################################################################
import asyncio
import websockets

async def send_command_and_receive_response():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            command = input("Enter the command to send to the server (e.g., check_service_status): ")
            await websocket.send(command)
            response = await websocket.recv()
            print(f"Received response from server:\n{response}")

asyncio.get_event_loop().run_until_complete(send_command_and_receive_response())
'''

import asyncio
import websockets

async def send_command_and_receive_response():
    uri = "ws://google.com:80"
    async with websockets.connect(uri) as websocket:
        while True:
            command = input("> ")
            await websocket.send(command)
            response = await websocket.recv()
            print(response)

asyncio.get_event_loop().run_until_complete(send_command_and_receive_response())