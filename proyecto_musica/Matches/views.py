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

        userMatchWithUserBeingMatched = User_Matches.objects.filter( other_user=CurrentUser, is_active=True)

        userMatchWithUserMatching = User_Matches.objects.filter(current_user=CurrentUser, is_active=True)


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
            serialized_data['id'] = match.like_id


            user_objects.append(serialized_data)


        res = {'success' : True, 'Matches ': user_objects}

        return response.Response(res, status=status.HTTP_200_OK)


class UnMatchView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):

        CurrentUser = request.user

        # look for the user
        try:
            unmatchedUser = User.objects.get(username=id)
            # makes sure tha t
            if CurrentUser == unmatchedUser:
                raise User.DoesNotExist

        except User.DoesNotExist:
            res = {'success' : True, 'user': None}
            return response.Response(res, status=status.HTTP_200_OK)


        # look for the matches that are currently active
        userMatchWithUserBeingMatched = User_Matches.objects.filter(current_user=CurrentUser, other_user=unmatchedUser, is_active=True)

        userMatchWithUserMatching = User_Matches.objects.filter(current_user=unmatchedUser, other_user=CurrentUser, is_active=True)



        if userMatchWithUserBeingMatched:
            match = userMatchWithUserBeingMatched[0]
            match.is_active = False
            match.save()
        elif userMatchWithUserBeingMatched:
            match = userMatchWithUserMatching[0]
            match.is_active = False
            match.save()



        res = {'success' : True, 'isMatch ': False, 'user': {}}

        return response.Response(res, status=status.HTTP_201_CREATED)
