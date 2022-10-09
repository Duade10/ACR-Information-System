import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class SocketConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.room_group_name = "broadcast"
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

    # def disconnect(self, close_code):
    #     # Leave room group
    #     async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
    #     super().disconnect("close")

    def establish_socket(self, event):
        message = event["message"]
        reload_type = event["reload_type"]
        self.send(text_data=json.dumps({"type": "reload", "message": message, "reload_type": reload_type}))
