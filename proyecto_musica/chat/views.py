from django.shortcuts import render
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from chat.models import Inbox
from authentication.models import User



import hashlib

# this gets the inbox of the user
class InboxView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        usr1 = '051fe3f37ca249639aa8a4e38ed0b556'
        usr2 = '218241e0ede946fd90d1401144d1044c'
        sss = (usr2+usr1).encode()

        #218241e0ede946fd90d1401144d1044c
        # m = hashlib.md5()
        #
        # str2 = usr1 + usr2
        # print(str2)
        # m.update('123')
        # str(int(m.hexdigest(), 16))[0:12]

        # this works
        my_hash = hashlib.md5(sss).hexdigest()
        print(my_hash)
        if my_hash == 'ec546e6b7b8897caff42d47b86369fc6':
            print("the hash is true")


        m = hashlib.md5()
        m.update(sss)
        print(str(int(m.hexdigest(), 16))[0:12])

        res = {'success' : True, 'hash': 'aHash'}

        return response.Response(res)

        # crete an inbox as soon as you send a message



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


        # print("logged in user :", user_to_Sender)
        m = hashlib.md5()
        m.update(user_to_Sender)

        hashed_str = str(int(m.hexdigest(), 16))[0:12]

        inbox_count = Inbox.objects.filter(inbox_user_to_sender=hashed_str).count()

        if inbox_count > 0:
            res = {'success' : False, 'error' : "inbox already exists"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)





        inbox_obj = Inbox(user_id=user,sender_id=user_obj,inbox_user_to_sender=hashed_str)
        inbox_obj.save()

        # print("reciver in user :", user_obj.id.hex)







        #receiver_user = (User.objects.filter(id=receiver_id).values('id'))[0]['id']

        # print(receiver_user)






        res = {'success' : True, 'message': 'message has been created'}
        return response.Response(res, status=status.HTTP_201_CREATED)
