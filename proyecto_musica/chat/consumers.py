import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from rest_framework import response, status, permissions



class ChatConsumer(WebsocketConsumer):

    permission_classes = (permissions.IsAuthenticated,)

    def fetch_messages(self, data):
        # get the last ten messages or so
        messages = 'this is the server replying back to you'
        content = {
            'command': 'messages',
            'messages': messages
        }
        self.send_message(content)


    def connect(self):
        self.user = self.scope["user"]
        print("self user", self.user)
        print("self.scope", self.scope)

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        print(self.room_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def new_message(self, data):
        print('new message: ',data )

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        permission_classes = (permissions.IsAuthenticated,)
        print(permission_classes)
        print("receiving", text_data)
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

        #text_data_json = json.loads(text_data)

        #message = text_data_json["message"]

              # Send message to room group
        #async_to_sync(self.channel_layer.group_send)(
        #    self.room_group_name, {"type": "chat_message", "message": message}
        #)

    def send_message(self, message):
        print("sending message")
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
