from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from rest_framework import response
from authentication.models import User

from newsfeed.models import User_Matches, User_Likes


from Matches.serializers import MatchesSerializer

class MatchesView(GenericAPIView):
    # this will get all of the matches
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        CurrentUser = request.user


        # will get all of the matches that the user has
          # this matches have to be where is_active is true

        userMatchWithUserBeingMatched = User_Matches.objects.filter( other_user=CurrentUser)

        userMatchWithUserMatching = User_Matches.objects.filter(current_user=CurrentUser)


        combinedMatches = (userMatchWithUserBeingMatched | userMatchWithUserMatching).order_by('-created_at')

        url = request.build_absolute_uri()
        newurl = str(url)

        base_url = newurl[:-8] + ''

        # for every match we must return:
        # the video of the user
        # username
        # and the message sent

        user_objects = []

        for match in combinedMatches:
            matchedUser = None

            if match.current_user == CurrentUser:
                matchedUser = match.other_user
            else:
                matchedUser = match.current_user


            serializer = MatchesSerializer(matchedUser, context = {'request': request, 'base_url': base_url})


            # getting the matches
            theLike = User_Likes.objects.filter(userLiking=matchedUser, userTwo=CurrentUser)[0]


            # refactor this
            serialized_data = serializer.data
            serialized_data['message'] = theLike.message

            user_objects.append(serialized_data)


        res = {'success' : True, 'Matches ': user_objects}

        return response.Response(res, status=status.HTTP_200_OK)


class UnMatchView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):

        res = {'success' : True, 'isMatch ': False, 'user': {}}

        return response.Response(res, status=status.HTTP_201_CREATED)
