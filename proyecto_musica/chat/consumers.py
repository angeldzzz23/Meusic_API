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
from authentication.models import User
from api.models import Images

roomsMap = {}

# roomsMap = {
#            room_group_name = ["userID1", "userID2..."]
#            }


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.listOfUsers = []
        self.user = self.scope["user"]

        print(self.user)


        # if self.user.is_anonymous: 
        #     await self.close()
        #     return
        
        # print("User is: ", self.user.id)

        # try:
        #     self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        #     self.room_group_name = f"chat_{self.room_name}"
        # except:
        #     print("Not in the room yet1")

        # try:
        #     if self.user.id not in roomsMap[self.room_name]:
        #         roomsMap[self.room_name].append(self.user.id)
        # except (KeyError):
        #     roomsMap[self.room_name] = []
        #     roomsMap[self.room_name].append(self.user.id)
        # except (AttributeError):
        #     print("Not in the room yet2")



        # # Join room group
        # try:
        #     await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        #     # await self.accept()
        # except:
        #      print("Not in the room yet")
             
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        try:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        except:
            print("Not in the room yet3")

        #await self.close()



    # TODO: save the data in the
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


    # this function calls chat_message
    async def new_message(self, data): 
        print(self.user.username )
        message = data["message"]
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", 
                                    "message": message,
                                    "user_username": self.user.username        # Pass the sender id here
                                    }
        )



    @database_sync_to_async
    def fetch_inbox(self, data):
        requestingUser = self.user.id
        print("Fetch User Inbox: ", requestingUser)
        inboxes = []

        arrayOfUserInboxes = Inbox.objects.filter(Q(sender_id_id=requestingUser)|Q(user_id_id=requestingUser)).values_list('inbox_user_to_sender', 'inbox_id', 'sender_id_id', 'user_id_id')

        for element in arrayOfUserInboxes:
            inboxHash, inboxID, sender, recepient = element

            if sender == self.user.id:
                trueRecepient = recepient
            else:
                trueRecepient = sender

            recepientFirstName = User.objects.filter(id=trueRecepient).values_list('first_name')[0][0]
            recepientLastName  = User.objects.filter(id=trueRecepient).values_list('last_name')[0][0]

            fullName = recepientFirstName + ' ' + recepientLastName

            #image_url = Images.objects.filter(user_id=trueRecepient).values_list('url')[0]

            currentInboxInfo = {
                                'inbox_id':   inboxID,
                                'inbox_hash': inboxHash,
                                'recepient':  fullName,
                                #'image_url':  image_url
            }
            inboxes.append(currentInboxInfo)

        print("This is the inboxes of a user: ", inboxes)


    commands = {
        'new_message': new_message,
        'fetch_inbox': fetch_inbox,
    }




    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]
        user_sender_id = self.user.id
        user_receiver_id = self.user.id

        await self.commands[text_data_json['command']](self, text_data_json)



        # # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name, {"type": "chat_message", 
        #                             "message": message,
        #                             "user_username": self.user.username        # Pass the sender id here
        #                             }
        # )

 



    @database_sync_to_async
    def handleMessage(self, sender_id, message):

        #inbox_hash = '104592537104'


        for userID in roomsMap[self.room_name]:
            if userID==sender_id:
                currentSender = userID
                print("This is sender id ", currentSender)
            else:
                currentReceiver = userID
                print("This is receiver id ", currentReceiver)


        
        #Retrieving the inbox hash
        try:
            # The inbox already exists
            #currentHash = Inbox.objects.filter(sender_id_id=currentSender, user_id_id=currentReceiver).values_list('inbox_user_to_sender')[0][0] 
            currentHash = Inbox.objects.filter(Q(sender_id_id=currentSender, user_id_id=currentReceiver) | Q(sender_id_id=currentReceiver, user_id_id=currentSender)).values_list('inbox_user_to_sender')[0][0] 
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



        # print("TESTING THE 10 messages function: \n\n")

        # print(get_last_10_messages(currentHash))

