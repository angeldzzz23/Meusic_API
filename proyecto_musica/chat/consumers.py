import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Inbox

from rest_framework import response, status, permissions
from django.db.models import Q



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

    def fetch_inbox(self, data):
        # get the id of the user
        used_id = data['id']

        inboxes = Inbox.objects.filter(Q(user_id=used_id) | Q(sender_id=used_id))




        content = {
            'command': 'inboxes',
            'messages': self.inboxes_to_json(inboxes)
        }

        self.send_message(content)


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'fetch_inbox' : fetch_inbox
    }

    def inboxes_to_json(self, inboxes):
        result = []
        for inbox in inboxes:
            result.append(self.inbox_to_json(inbox))
        return result

    def inbox_to_json(self, inbox):
        return {
            'inbox_id': inbox.inbox_id,
            'user_id': str(inbox.user_id.id),
            'sender_id': str(inbox.sender_id.id),
            'latest_message': str(inbox.latest_message),
            'date_modified': str(inbox.date_modified),
            'unseen_messages': str(inbox.unseen_messages),
            'inbox_user_to_sender': str(inbox.inbox_user_to_sender)
        }

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
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
