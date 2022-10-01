from rest_framework import serializers
from chat.models import Inbox
from authentication.models import User


class InboxesSerializer(serializers.ModelSerializer):
    inbox = serializers.SerializerMethodField()
    class Meta:
        model = Inbox
        fields = ('inbox',)

    def get_inbox(self, obj):
        user_id = (User.objects.filter(email=obj.email).values('id'))[0]['id']

        # getting the inbox when the user has been the receiver
        # and also when the user has been the senter
        inbox_nums = Inbox.objects.filter(user_id=user_id).order_by('date_modified').values('inbox_id','user_id', 'sender_id', 'unseen_messages', 'date_modified',)
        inbox_receiver = Inbox.objects.filter(sender_id=user_id).order_by('date_modified').values('inbox_id','user_id', 'sender_id', 'unseen_messages', 'date_modified',)

        union_of_inbox = inbox_nums | inbox_receiver

        return union_of_inbox
