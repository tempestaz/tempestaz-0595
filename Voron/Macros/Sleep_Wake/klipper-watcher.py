#!/usr/bin/env python3
import asyncio
import websockets
import json
import aiohttp

MOONRAKER_HOST = "http://localhost:7125"

STATE_TO_MACRO = {
    "ready": "WAKE_UP",             # printer fully initialized
    "shutdown": "PRINTER_SHUTDOWN",
    "error": "PRINTER_ERROR",
    "startup": "PRINTER_STARTUP",
    "disconnected": "PRINTER_DISCONNECTED",
}

async def call_macro(macro_name):
    async with aiohttp.ClientSession() as session:
        url = f"{MOONRAKER_HOST}/printer/gcode/script"
        payload = {"script": macro_name}
        async with session.post(url, json=payload) as resp:
            print(f"Called {macro_name}:", await resp.text())

async def listen_for_states():
    uri = f"ws://{MOONRAKER_HOST.split('//')[1]}/websocket"
    while True:
        try:
            async with websockets.connect(uri) as ws:
                await ws.send(json.dumps({
                    "jsonrpc": "2.0",
                    "method": "printer.objects.subscribe",
                    "params": {"objects": {"printer": ["state"]}},
                    "id": 1
                }))
                async for msg in ws:
                    data = json.loads(msg)
                    try:
                        state = data["params"][0]["printer"]["state"]
                        print("Detected state:", state)
                        if state in STATE_TO_MACRO:
                            await call_macro(STATE_TO_MACRO[state])
                    except (KeyError, IndexError):
                        continue
        except Exception as e:
            print("Connection error:", e)
            await asyncio.sleep(5)

asyncio.run(listen_for_states())
