from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from rest_framework import response
from authentication.models import User, Locations
from authentication.serializers import RegisterSerializer

from newsfeed.models import User_Matches,User_Likes
# importing the serialziers
from newsfeed.serializers import ProfileSerializer

# from django.contrib.gis.db.models import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point



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

        url  = request.build_absolute_uri()
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
# https://stackoverflow.com/questions/19703975/django-sort-by-distance
from django.contrib.gis.geos import GEOSGeometry

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.distance import great_circle
from math import sin, cos, radians, acos


EARTH_RADIUS_IN_MILES = 3958.761

def calc_dist_fixed(lat_a, long_a, lat_b, long_b):
    """all angles in degrees, result in miles"""
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    delta_long = radians(long_a - long_b)
    cos_x = (
        sin(lat_a) * sin(lat_b) +
        cos(lat_a) * cos(lat_b) * cos(delta_long)
        )
    return acos(cos_x) * EARTH_RADIUS_IN_MILES

class Feed(GenericAPIView):

    # permission_classes = (permissions.IsAuthenticated,)
    # work on a basic algithm for this


    def get(self, request):

        # the location of the user
        newport_ri = (34.068207555435585, -118.16539005397912)
        cleveland_oh = (34.586079138685875, -117.41845574395259)

        print(calc_dist_fixed(34.068207555435585, -118.16539005397912, 34.586079138685875, -117.41845574395259))


        print(great_circle(newport_ri, cleveland_oh).miles)



        # Priority 





        # get the most recent location of the user
        # user = request.user
        #
        # # # longitude and latitude
        # pnt = GEOSGeometry('POINT(-121.47769260984167 38.5746849063679)', srid=4326)
        #
        # p = Locations(point=pnt, user=user)
        # p.save()

        # user_location = Locations.objects.filter(user=user).last()

        # qs = Locations.objects.filter(geometry__dwithin=(GEOSGeometry('POINT(-121.47769260984167 38.5746849063679)'), D(m=5000)))

        # print(len(qs))


        # n = Event.obiects.annotate distance Distance 'location', user_location)).order_by('-distance')

        # pnt = Point(float(-121.47769260984167), float(38.5746849063679), srid=4326)

        # pnt = Point(float(-121.47769260984167), float(38.5746849063679), srid=4326)


        # pnt = GEOSGeometry('POINT(-96.876369 29.905320)', srid=4326)
        #
        # qs = Locations.objects.filter(point__distance_lte=(pnt, D(km=50)))

        # print(len(qs))

        # qs = Locations.objects.filter(geometry__dwithin=(location.geometry, 0.05))

        # Locations.objects.filter(location_distance_lt=(pnt, D(km=radius)))
        # print(qs)
        # print(qs.count())


         # Distance(m=distance(pnt, self.user_b.profile.location).meters)

        # user_location = Locations.objects.filter(user=user).last()

        # now we filter through all of those but exclude the user
        # location_objects = Locations.objects.filter(location__distance_lte=(user_location, Distance(mi=radius)))

        # qs = Locations.objects.filter(location__distance_lte=(user_location, Distance(10)))
        #
        #
        #
        # location_objects = Locations.annotate(distance-Distance('location', user_location)).ord
        #
        #
        #
        #
        # print(location_objects)

        # ref_location = user_location

        # qs = Locations.objects.filter(location__distance_lte=(user_location, D(10)))



        # n = Locations.objects.filter(location__distance_lte=(ref_location,D(m=2000)))


# django.core.exceptions.FieldError: Cannot resolve keyword 'location' into field. Choices are: created_at, location_id, point, user, user_id




        # then we compare them to the other users

        #print the locations



         # all_users = User.objects.all().exclude(id=request.user.id).exclude(is_staff=True)



         # user_objects = []
         #
         # url = request.build_absolute_uri()
         # newurl = str(url)
         # base_url = newurl[:-5] + ''
         #
         # for user in all_users:
         #
         #    serializer = ProfileSerializer(user, context = {'request': request, 'base_url': base_url})
         #    serialized_data = serializer.data
         #    user_objects.append(serialized_data)
         #
         # theFeedJson = {'feed': user_objects}

        theFeedJson = {'feed': 'there is not hahasha'}
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
