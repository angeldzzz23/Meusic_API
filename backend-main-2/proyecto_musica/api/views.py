from django.shortcuts import render


from rest_framework.views import APIView

#imports the response class
from rest_framework.response import Response

# we can use the status codes when using our post method handlers
from rest_framework import status

from api import serializers

from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# makes sure that a viewset is read only, if the user is not authenticated
#from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated



from api import models
from api import permissions



class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handle creating and updating profiles"""
    serializer_class = serializers.UserProfilesSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,) # comma creates
    permission_classes = (permissions.UpdateOwnProfile,) # adds the permission class
    # adding search feature
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


#
class UserLoginApiView(ObtainAuthToken):
    """ Handle creating user authentication """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated

    )

    def perform_create(self,serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
