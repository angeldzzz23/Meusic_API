from rest_framework import serializers
from chat.models import Inbox
from chat.models import Chat
from authentication.models import User

class ChatsSerializer(serializers.ModelSerializer):
    convo = serializers.SerializerMethodField()
    class Meta:
        model = Chat
        fields = ('convo',)


    def get_convo(self, obj):
        # print(obj)
        print(" before sqsnqjnsqjnsjqnsjqnsjq")
        print(Inbox.objects.filter(inbox_user_to_sender=obj))
        print(" After sqsnqjnsqjnsjqnsjqnsjq\n\n\n\n")
        conversation = Chat.objects.filter(inbox_user_to_sender=obj).values('message_id', 'message','sender_id', 'created_at', )
        return conversation



class InboxesSerializer(serializers.ModelSerializer):
    inbox = serializers.SerializerMethodField()
    class Meta:
        model = Inbox
        fields = ('inbox',)


    def get_inbox(self, obj):
        user_id = (User.objects.filter(email=obj.email).values('id'))[0]['id']

        # getting the inbox when the user has been the receiver
        # and also when the user has been the senter
        inbox_nums = Inbox.objects.filter(user_id=user_id).order_by('date_modified').values('inbox_id','user_id', 'sender_id', 'unseen_messages', 'date_modified','inbox_user_to_sender','latest_message')
        inbox_receiver = Inbox.objects.filter(sender_id=user_id).order_by('date_modified').values('inbox_id','user_id', 'sender_id', 'unseen_messages', 'date_modified','inbox_user_to_sender','latest_message' )
        if inbox_nums.count() == 0 and inbox_receiver.count() == 0:
            return inbox_receiver


        union_of_inbox = inbox_nums | inbox_receiver

        return union_of_inbox