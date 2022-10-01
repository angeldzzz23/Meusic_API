from django.shortcuts import render

from django.db import models
from authentication.models import User

# id
# user_id
# seen, is either True or false
# unseen messages
# unseen numbers (number of messages that have been seen)
# last message - latest message by date
# inboxhash user_id and the id put together



class Inbox(models.Model):
    inbox_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='inbox_id'
        )

    # the user that is receiving the message
    user_id = models.ForeignKey(
         User,
         on_delete=models.CASCADE,
         verbose_name='user_id',
         null=True,
         related_name='user'
    )

    # the user the starts the message 1
    sender_id = models.ForeignKey(
         User,
         on_delete=models.CASCADE,
         verbose_name='sender_id',
         null=True,
         related_name='sender'
    )
    # last message - latest message by date
    latest_message = models.CharField(max_length=1000, null=True)


    #  # number of unseen messages
    unseen_messages = models.IntegerField(default=0)

    # date modified
    date_modified = models.DateTimeField(auto_now=True)

    # we hashed user_id + sender_id
    inbox_user_to_sender = models.CharField(max_length=1000, null=True)
