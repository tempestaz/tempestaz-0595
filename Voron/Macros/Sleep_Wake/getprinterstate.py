
#This is just a test function to see if we can get the printer state from Moonraker via WebSocket
# It is not used in the main klipper-watcher.py script
import asyncio
import websockets
import json

# Function to get the printer state from Moonraker via WebSocket
async def get_printer_state():
    url = "ws://localhost:7125/websocket"  # Moonraker WebSocket endpoint

    try:
        # Connect to the WebSocket
        async with websockets.connect(url) as websocket:
            print("Connected to Moonraker WebSocket.")

            # Send a JSON-RPC message to query the printer state
            request = {
                "jsonrpc": "2.0",
                "method": "printer.objects.subscribe", #query", #.query",  # You can use 'printer.info' as well
                "params": {
                "objects": {
                    "idle_timeout": ["state"]
                    }
                },
                "id": 99
            }
            await websocket.send(json.dumps(request))  # Send the query as JSON

            # Wait for the response
            response = await websocket.recv()
            print("Received response:", response)

            # Optionally, parse the response if you expect JSON data
            try:
                response_data = json.loads(response)
                printer_state = response_data.get("result", {}).get("status").get("idle_timeout").get("state")
                print("Printer State:", printer_state)
            except json.JSONDecodeError:
                print("Error parsing JSON response.")

    except Exception as e:
        print(f"Error connecting to Moonraker WebSocket: {e}")

# Run the WebSocket test
asyncio.run(get_printer_state())
