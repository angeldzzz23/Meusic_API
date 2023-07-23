from django.shortcuts import render, redirect
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
from django.shortcuts import render
import hashlib
from django.db.models import Q
from channels.layers import get_channel_layer
from django.contrib.sessions.models import Session
from django.contrib.auth import SESSION_KEY
from django.conf import settings




def fetch_user_inbox(request):
    requestingUser = request.user.id
    print("Fetch User Inbox: ", requestingUser)
    inboxes = []

    arrayOfUserInboxes = Inbox.objects.filter(Q(sender_id_id=requestingUser)|Q(user_id_id=requestingUser)).values_list('inbox_user_to_sender', 'inbox_id', 'sender_id_id', 'user_id_id')

    for element in arrayOfUserInboxes:
        inboxHash, inboxID, sender, recepient = element

        if sender == request.user.id:
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

    return inboxes


from django.contrib.auth import get_user

def index(request):
    inboxes = fetch_user_inbox(request)
    inboxDict = {}
    for element in inboxes:
        currentInboxId = str(element['inbox_id'])
        inboxDict[currentInboxId] = element

    print("INBOXESSSS: ", inboxes)
    print("Session user: ", request.session.session_key)

    user = request.user.id
    print("USR", user)


    # session_engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
    # session_wrapper = session_engine.SessionStore(request.session.session_key)
    # session = session_wrapper.load()
    #user_id = session.get(SESSION_KEY)



    #print("CUrrent username: ", request.user.id)
    #user_id = get_user(request.session.get('_auth_user_id'))
    #print("USER cehck ", request.session.session_key['user_id'])



    return render(request, "chat/index.html", {'inboxDict': inboxDict})




def room(request, room_name):
    hashValue = Inbox.objects.filter(inbox_id=room_name).values_list('inbox_user_to_sender')[0][0]
    myMessages = Chat.objects.filter(inbox_user_to_sender=hashValue).values_list('message', 'sender_id_id')
    room_name = {
    "room_name": str(room_name),
    "messages": {}
    }

    for element in myMessages:
        #print("Message: ", element[0], "User: ", element[1])
        print("CUrrent message considered.    ", "USER REQUEST ID: ", request.user.id, "ELEMENT: ", element[1])
        if request.user.id == element[1]:
            messageUser = 'you'
        else:
            messageUser = 'recepient'

        room_name['messages'][str(element[0])] = messageUser

    print("CURRENT STATE OF ROOM-NAME: ", room_name)

    return render(request, "chat/room.html", {"room_name": room_name})


def anonymous_user(request):
    return render(request, "chat/not-authenticated.html")


def get_last_10_messages(inbox_hash):
    messages = Chat.objects.filter(inbox_user_to_sender=inbox_hash)
    return messages.order_by('-created_at').all()[:10]



def createHashedString(senderID, recepientID):
    user_to_Sender = (senderID.hex + recepientID.hex).encode()
    sender_to_user = (recepientID.hex + recepientID.hex).encode()


    m = hashlib.md5()
    m.update(user_to_Sender)
    hashed_str = str(int(m.hexdigest(), 16))[0:12]

    m2 = hashlib.md5()
    m2.update(sender_to_user)
    hashed_str2 = str(int(m2.hexdigest(), 16))[0:12]

    return hashed_str




# chat method
class ChatView(GenericAPIView):
    # retrieves all of the chats between two users
    # this requites the hashed chat
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        jd = request.data
        inbox_hash = jd['inbox_hash']
        print("INBOX HASH: ", inbox_hash)
        serializer = ChatsSerializer(inbox_hash)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

    def post(self, request):
        jd = request.data
        user = request.user

        inbox_hash = jd['inbox_user_to_sender']
        message = jd['message']

        inbox_count = Inbox.objects.filter(inbox_user_to_sender=inbox_hash).count()
        print("inbox_count: ", inbox_count)

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

    def post(self, request):
        jd = request.data
        user = request.user
        print("ID: ", user.id)

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











