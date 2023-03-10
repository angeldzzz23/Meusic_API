from django.db import models

from authentication.models import User

# this contains all of the user likes for all of the user
class User_Likes(models.Model):

    like_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='like_id'
    )

    # this is the user liking
    userLiking = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='userLiking',
        null=True,
        related_name='userLiking'
    )

    userTwo = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='userTwo',
        null=True,
        related_name='userTwo'
    )

    message = models.CharField(
    max_length=300,
    null=True,
    verbose_name='message'
    )

    created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='created_at'
    )

    class Meta:
        db_table = 'User_Likes'

# this database contains all of the matches for the users
# when the user unmatches the other user
class User_Matches(models.Model):

    like_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='like_id'
    )

    current_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='current_user',
        null=True,
        related_name='current_user'
    )

    other_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='other_user',
        null=True,
        related_name='other_user'
    )

    # when either user unmatches this is changed
    is_active = models.BooleanField( ('active'), default=True)

    created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='created_at'
    )

    class Meta:
        db_table = 'User_Matches'
