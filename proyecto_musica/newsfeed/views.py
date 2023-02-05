from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from rest_framework import response
from authentication.models import User
from authentication.serializers import RegisterSerializer

from newsfeed.models import User_Matches,User_Likes
# importing the serialziers
from newsfeed.serializers import ProfileSerializer


# this is in charge of showing the profile of the user
# user needs to be logged in.
class SeeProfileOfUserView(GenericAPIView):

    # this returns the public profile of a user in the newsfeed
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request,id):

        try:
            user = User.objects.get(username=id)

        except User.DoesNotExist:
            res = {'success' : True, 'user': None}
            return response.Response(res, status=status.HTTP_200_OK)


        serializer = RegisterSerializer(user)
        serialized_data = (serializer.data).copy()
        if 'gender' in serializer.data:
            serialized_data.pop('gender')

        del serialized_data['email']
        # del serialized_data['user']['email']


        res = {'success' : True, 'user': serialized_data}

        return response.Response(res, status=status.HTTP_201_CREATED)


# this will get the profile of the user.
class SeeUserView(GenericAPIView):
    # where id is the username
    # if the user does not have a valid username, then
    def get(self, request,id):

        try:
            user = User.objects.get(username=id)

        except User.DoesNotExist:
            res = {'success' : True, 'user': None}
            return response.Response(res, status=status.HTTP_200_OK)

        url = request.build_absolute_uri()
        newurl = str(url)
        base_url = newurl[:-(len(user.username) +5)] + ''
        print('new base url', base_url)



        serializer = ProfileSerializer(user, context = {'request': request, 'base_url': base_url})

        # make sure there is a profile image and a a video at least
        serialized_data = serializer.data

        print('data: ', serialized_data)


        if serialized_data['pictures'] == None or serialized_data['video'] == None:
            res = {'success' : True, 'user': None}
            return response.Response(res, status=status.HTTP_200_OK)

        res = {'success' : True, 'user': serialized_data}

        return response.Response(res, status=status.HTTP_200_OK)


# the newsfeed
# this will get the feed view
class Feed(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

         all_users = User.objects.all().exclude(id=request.user.id).exclude(is_staff=True)

         user_objects = []

         url = request.build_absolute_uri()
         newurl = str(url)
         base_url = newurl[:-5] + ''

         for user in all_users:

            serializer = ProfileSerializer(user, context = {'request': request, 'base_url': base_url})
            serialized_data = serializer.data
            user_objects.append(serialized_data)

         theFeedJson = {'feed': user_objects}

         return response.Response(theFeedJson, status=status.HTTP_200_OK)


class LikingView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):

        CurrentUser = request.user
        jd = request.data

        # you want to check if the user with that username has liked you before.
        try:
            userBeingLiked = User.objects.get(username=id)
            if userBeingLiked == CurrentUser:
                 raise User.DoesNotExist

        except User.DoesNotExist:
            res = {'success' : False, 'error': 'invalid user'}
            return response.Response(res, status=status.HTTP_200_OK)

        # query the likes table to see if the the user passed in the request has liked the current user before
        likesWithCurrentUserSecond = User_Likes.objects.filter(userLiking=userBeingLiked, userTwo=CurrentUser)

        # check if you have liked the user in the past
        likesWithcurrentUserFirst = User_Likes.objects.filter(userLiking=CurrentUser, userTwo=userBeingLiked)

        # # verifies if you have liked the user in the past
        if likesWithcurrentUserFirst:
            theFeedJson = {'success': False,
                            'message': 'this user has has been liked before'
                          }
            return response.Response(theFeedJson, status=status.HTTP_200_OK)


        # the user hasnt liked you before
        if not likesWithCurrentUserSecond:
            message = None

            if 'message' in jd:
                message = jd['message']

            # you create the record with the like
            like = User_Likes(userLiking=CurrentUser, userTwo=userBeingLiked, message=message)
            like.save()

            theFeedJson = {'success': True,
                            'isMatch': False
                          }

            return response.Response(theFeedJson, status=status.HTTP_201_CREATED)

        else: # the user has liked you before.



            userBeingLikedLike = likesWithCurrentUserSecond[0]
            message = userBeingLikedLike.message

            # TODO: create an inbox here with the messages

            # creating the user like and user matches record
            like = User_Likes(userLiking=CurrentUser, userTwo=userBeingLiked, message=message)
            like.save()

            match = User_Matches(current_user=CurrentUser,other_user=userBeingLiked)
            match.save()


            theFeedJson = {'success': True,
                            'isMatch': True,
                            'user' : {
                                'username': userBeingLiked.username,
                                'message': message
                            }
                          }

        return response.Response(theFeedJson, status=status.HTTP_200_OK)
