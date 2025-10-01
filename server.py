import asyncio
import websockets
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8765))

connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    print(f"Connected Client: {websocket.remote_address} (path: {websocket.request.path})")

    try:
        async for message in websocket:
            print(f"Recive from {websocket.remote_address}: {message}")
            for client in connected_clients:
                await client.send(message)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection Closed: {websocket.remote_address} (code: {e.code}, reason: {e.reason}")
    finally:
        connected_clients.remove(websocket)

async def main():
    print(f"Server Starting... : ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server Stopped...")
