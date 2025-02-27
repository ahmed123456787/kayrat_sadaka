from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs
from .middlware import get_user_from_token

class MosqueNotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connection request received.")

        # Extract token from headers or query string
        token = await self.get_token()
        if not token:
            print("No valid token provided.")
            await self.close(code=4001)
            return

        # Authenticate user
        user = await get_user_from_token(token)
        if not user or user.is_anonymous:
            print(" Authentication failed.")
            await self.close(code=4001)
            return

        self.scope['user'] = user

        # Extract mosque ID from URL
        self.mosque_id = self.scope["url_route"]["kwargs"].get("mosque_id")
        if not self.mosque_id:
            print(" Mosque ID missing.")
            await self.close(code=4002)
            return

        self.group_name = f"mosque_{self.mosque_id}"

        # Join the group
        if hasattr(self.channel_layer, "group_add"):
            await self.channel_layer.group_add(self.group_name, self.channel_name)

        print(f"User {user} connected to group {self.group_name}.")
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name") and hasattr(self.channel_layer, "group_discard"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"🔹 User disconnected with code {close_code}.")

    async def receive(self, text_data):
        # Handle incoming messages (if needed)
        print(f"📩 Received data: {text_data}")

    async def send_notification(self, event):
        # Send notification to the WebSocket
        message = event.get("message", "No message provided")
        await self.send(text_data=json.dumps({"message": message}))

    async def get_token(self):
        """
        Extracts the token from the WebSocket headers or query string.
        """
        # Check headers
        headers = dict(self.scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode()

        if auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]

        # Check query string
        query_string = self.scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        return params.get("token", [None])[0]
