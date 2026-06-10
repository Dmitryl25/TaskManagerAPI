class ConnectionManager:
    def __init__(self):
        self.connections = {}

    def connect(self,
                user_id: str,
                websocket):
        if user_id not in self.connections:
            self.connections[user_id] = []
        self.connections[user_id].append(websocket)

    def disconnect(self,
                   user_id: str,
                   websocket):
        self.connections[user_id].remove(websocket)

    async def send_message(self,
                           user_id: str,
                           message: str):
        for websocket in self.connections.get(user_id, []):
            await websocket.send_text(message)

manager = ConnectionManager()