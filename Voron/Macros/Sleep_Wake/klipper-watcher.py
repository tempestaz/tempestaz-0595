
#!/usr/bin/env python3
import asyncio
import websockets
import json
import aiohttp

MOONRAKER_HOST = "http://localhost:7125"

STATE_TO_MACRO = {
    "Ready": "WAKE_UP",             # printer fully initialized
    "Printing": "PRINTER_PRINTING",
    "Idle": "PRINTER_IDLE",   
}

async def call_macro(macro_name):
    async with aiohttp.ClientSession() as session:
        url = f"{MOONRAKER_HOST}/printer/gcode/script"
        payload = {"script": macro_name}
        async with session.post(url, json=payload) as resp:
            print(f"Called {macro_name}:", await resp.text())

async def listen_for_states():
    uri = f"ws://{MOONRAKER_HOST.split('//')[1]}/websocket"
    print("URI:", uri)
    last_state = None
    while True:
        try:
            async with websockets.connect(uri) as ws:
                print("Connected to Moonraker WebSocket.")
                # Send a JSON-RPC message to query the printer state
                request = {
                    "jsonrpc": "2.0",
                    "method": "printer.objects.subscribe", 
                    "params": {
                        "objects": {
                            "idle_timeout": ["state"]
                        }
                    },
                    "id": 99
                }
                await ws.send(json.dumps(request))  # Send the query as JSON

                # Wait for the response
                response = await ws.recv()
                #print("Received response:", response)

                #async for msg in ws:
                try:
                    data = json.loads(response)
                    state = data["result"]["status"]["idle_timeout"]["state"]
                    print("Detected state:", state)
                    if state != last_state and state in STATE_TO_MACRO:
                        await call_macro(STATE_TO_MACRO[state])
                        last_state = state
                except json.JSONDecodeError:
                    print("Error: Invalid JSON response")
                except (KeyError, IndexError):
                    continue
                await asyncio.sleep(5)  # Poll every 5 seconds
        except Exception as e:
            print("Connection error:", e)
            await asyncio.sleep(5)

asyncio.run(listen_for_states())
