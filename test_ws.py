import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8001/ws/orders/"
    
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Sending ping action without PIN...")
            
            await websocket.send(json.dumps({"action": "ping"}))
            response = await websocket.recv()
            print(f"Response: {response}")
            
            print("\nSending ping action with test PIN (1234)...")
            await websocket.send(json.dumps({"action": "ping", "pin": 1234}))
            response = await websocket.recv()
            print(f"Response: {response}")
            
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
