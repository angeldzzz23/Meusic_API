from django.shortcuts import render
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from chat.models import Inbox
from chat.models import Chat
from authentication.models import User
from chat.serializers import InboxesSerializer
from chat.serializers import ChatsSerializer
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync



import hashlib


def get_last_10_messages(inbox_hash):
    messages = Chat.objects.filter(inbox_user_to_sender=inbox_hash)
    return messages.order_by('-created_at').all()[:10]


# chat method
class ChatView(GenericAPIView):
    # retrieves all of the chats between two users
    # this requites the hashed chat
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        jd = request.data
        inbox_hash = jd['inbox_hash']
        serializer = ChatsSerializer(inbox_hash)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

    def post(self, request):
        jd = request.data
        user = request.user

        inbox_hash = jd['inbox_user_to_sender']
        message = jd['message']

        inbox_count = Inbox.objects.filter(inbox_user_to_sender=inbox_hash).count()

        if inbox_count == 0:
            res = {'success' : False, 'error' : "current inbox does not exist"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        inbox = Inbox.objects.filter(inbox_user_to_sender=inbox_hash).update(latest_message=message)


        new_message = Chat(sender_id=user,message=message, inbox_user_to_sender=inbox_hash)
        new_message.save()


        res = {'success' : True, 'data': 'message was sent'}
        jd = request
        return response.Response(res, status=status.HTTP_201_CREATED)









# this gets the inbox of the user
class InboxView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # getting all of the user
        user = request.user
        serializer = InboxesSerializer(user)
        channel_layer = get_channel_layer()
        # for chat_name in chats:
        # print("here1")
        # async_to_sync(channel_layer.send)("chat_338217561529", { "type": "send.alert"})
        # print("here2")
        # async_to_sync(channel_layer.send)("338217561529", { "type": "send.alert"})
        #
        # print("here3")
        # async_to_sync(channel_layer.send)("chat", { "type": "send.alert"})
        # async_to_sync(channel_layer.send)("chat", { "type": "send.alert"})


        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


        # usr1 = '051fe3f37ca249639aa8a4e38ed0b556'
        # usr2 = '218241e0ede946fd90d1401144d1044c'
        # sss = (usr2+usr1).encode()

        #218241e0ede946fd90d1401144d1044c
        # m = hashlib.md5()
        #
        # str2 = usr1 + usr2
        # print(str2)
        # m.update('123')
        # str(int(m.hexdigest(), 16))[0:12]

        # this works
        # my_hash = hashlib.md5(sss).hexdigest()
        # print(my_hash)
        # if my_hash == 'ec546e6b7b8897caff42d47b86369fc6':
        #     print("the hash is true")
        #
        #
        # m = hashlib.md5()
        # m.update(sss)
        # print(str(int(m.hexdigest(), 16))[0:12])
        #
        # res = {'success' : True, 'hash': 'aHash'}
        #
        # return response.Response(res)

        # crete an inbox as soon as you send a message

    #
    def post(self, request):
        jd = request.data
        user = request.user

        last_message =  jd['message']
        receiver_id = jd['receiver_id']

        try:
            user_obj = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            res = {'success' : False, 'error' : "receiver id does not exist."}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        user_to_Sender = (user.id.hex + user_obj.id.hex).encode()
        sender_to_user = (user_obj.id.hex + user_obj.id.hex).encode()


        # print("logged in user :", user_to_Sender)


        m = hashlib.md5()
        m.update(user_to_Sender)
        hashed_str = str(int(m.hexdigest(), 16))[0:12]

        m2 = hashlib.md5()
        m2.update(sender_to_user)
        hashed_str2 = str(int(m2.hexdigest(), 16))[0:12]

        inbox_count = Inbox.objects.filter(inbox_user_to_sender=hashed_str).count()
        inbox_count_sender = Inbox.objects.filter(inbox_user_to_sender=hashed_str2).count()


        if inbox_count > 0 or inbox_count_sender > 0:
            res = {'success' : False, 'error' : "inbox already exists"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        # saving the inbox
        inbox_obj = Inbox(user_id=user_obj,sender_id=user,inbox_user_to_sender=hashed_str)
        inbox_obj.save()

        # print(receiver_user)
        res = {'success' : True, 'message': 'inbox has been created'}
        return response.Response(res, status=status.HTTP_201_CREATED)
