import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Inbox
from chat.models import Chat

from rest_framework import response, status, permissions
from django.db.models import Q
from authentication.models import User
from channels.db import database_sync_to_async

from chat.views import createHashedString
from chat.views import get_last_10_messages

roomsMap = {}

# roomsMap = {
#            room_group_name = ["userID1", "userID2..."]
#            }


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.listOfUsers = []
        self.user = self.scope["user"]

        if self.user.is_anonymous: await self.close()
        else:   print("User is: ", self.user.id)

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        try:
            if self.user.id not in roomsMap[self.room_name]:
                roomsMap[self.room_name].append(self.user.id)
        except (KeyError):
            roomsMap[self.room_name] = []
            roomsMap[self.room_name].append(self.user.id)


        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_sender_id = self.user.id
        user_receiver_id = self.user.id
        print("USER RECEIVE FUNCTION: ", self.user.id)      # This is the id of the user that sends a message

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", 
                                    "message": message,
                                    "user_username": self.user.username        # Pass the sender id here
                                    }
        )

        print("TEXT DATA JSON: ", text_data_json)


    async def chat_message(self, event):
        message = event["message"]

        # This defines sender and receiver
        if event["user_username"] == self.user.username: 
            user_sender_id = self.user.id
            await self.handleMessage(user_sender_id, message)
        else:
            user_receiver_id = self.user.id   
            

        print("DICT", roomsMap)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message} ))  

        # Put message into db
        #await self.handleMessage(user_sender_id, message)



    @database_sync_to_async
    def handleMessage(self, sender_id, message):

        #inbox_hash = '104592537104'

        for userID in roomsMap[self.room_name]:
            if userID==sender_id:
                currentSender = userID
                print("This is sender id ", userID)
            else:
                currentReceiver = userID
                print("This is receiver id ", userID)



        # Retrieving the inbox hash
        try:
            # The inbox already exists
            currentHash = Inbox.objects.filter(sender_id_id=currentSender, user_id_id=currentReceiver).values_list('inbox_user_to_sender')[0][0] 
        except IndexError:
            # The inbox does not exist yet. First we create a hashed string -> Then we create inbox
            currentHash = createHashedString(currentSender, currentReceiver)
            inbox = Inbox.objects.create(inbox_user_to_sender=currentHash, sender_id_id=currentSender, user_id_id=currentReceiver)
            inbox.save()


        # Then we update last message from the inbox
        inbox = Inbox.objects.filter(inbox_user_to_sender=currentHash).update(latest_message=message)

        # Then we add the message to the chat
        new_message = Chat.objects.create(sender_id_id=currentSender, message=message, inbox_user_to_sender=currentHash)
        new_message.save()



        print("TESTING THE 10 messages function: \n\n")

        print(get_last_10_messages(currentHash))

