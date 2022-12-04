import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Inbox
from chat.models import Chat

from rest_framework import response, status, permissions
from django.db.models import Q
from authentication.models import User

from .views import get_last_10_messages

class ChatConsumer(WebsocketConsumer):

    permission_classes = (permissions.IsAuthenticated,)

    def fetch_messages(self, data):
        # get the last ten messages or so
        messages = get_last_10_messages(data['inbox_hash'])

        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id_hash': str(message.inbox_user_to_sender),
            'author': str(message.sender_id.id),
            'content': str(message.message),
            'timestamp': str(message.created_at)
        }


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
        # save the message in the database
        # get the user id
        usrId = data["id"]
        message = data["content"]
        inbox_hash = data["inbox_hash"]

        foundUsr = User.objects.filter(id=usrId)

        if foundUsr.count() == 0:
            # return an error message
            print("returninn an error message ")
            return

        # save message to database
        # get the user given the id

        new_message = Chat(sender_id=foundUsr[0],message=message, inbox_user_to_sender=inbox_hash)
        new_message.save()

        content = {
            'command': 'messages',
            'messages': self.messages_to_json([messages])
        }
        self.send_message(content)



    def fetch_inbox(self, data):
        # get the id of the user
        used_id = data['id']
        print("checking type of id", type(used_id))
        inboxes = Inbox.objects.filter(Q(user_id=used_id) | Q(sender_id=used_id))

        content = {
            'command': 'inboxes',
            'messages': self.inboxes_to_json(inboxes, used_id)
        }

        self.send_message(content)


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'fetch_inbox' : fetch_inbox
    }

    def inboxes_to_json(self, inboxes, id):
        result = []
        for inbox in inboxes:
            result.append(self.inbox_to_json(inbox, id))
        return result

    def inbox_to_json(self, inbox,id):
        # we check if the user sent the message
        curUser = None

        if str(inbox.sender_id.id) == id:
            curUser = inbox.user_id
            print("they are the same ")
        elif str(inbox.user_id.id) == id:
            curUser = inbox.sender_id
            print("user is the user_id")

        return {
            'inbox_id': inbox.inbox_id,
            'user_id': self.user_to_json(curUser),
            'latest_message': str(inbox.latest_message),
            'date_modified': str(inbox.date_modified),
            'unseen_messages': str(inbox.unseen_messages),
            'inbox_user_to_sender': str(inbox.inbox_user_to_sender)
        }

    # converts the user to json
    def user_to_json(self,curUser):
        #lsksks
        return  {
            'user_id': str(curUser.id),
            'first_name': str(curUser.first_name),
            'last_name': str(curUser.last_name)
        }

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    async def send_alert(self, event):
        print("sending alert")
        # Send message to WebSocket
        await self.send(text_data={
            'type': 'alert',
            'details': 'An external API api.external.com needs some data from you'
        })


    # Receive message from WebSocket
    def receive(self, text_data):


        async_to_sync(self.channel_layer.group_send)( "chat",
        {
            "type": "chat.message",
            "text": text_data,
        },
        )

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
        print("yo")
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
