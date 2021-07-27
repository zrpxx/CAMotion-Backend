import websocket

websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws_algo/1")

ws.run_forever()