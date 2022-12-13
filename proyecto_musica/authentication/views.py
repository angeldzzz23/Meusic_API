from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer
from authentication.serializers import EditSerializer
from authentication.serializers import LoginSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from authentication.models import User, User_Skills, Skills, Genres, User_Genres, User_Artists, Genders, Verification
from authentication.functions import validate_field, List_Fields, User_Fields
from authentication.Util import Util
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Images
from api.models import Videos
from rest_framework.response import Response
import os
from pathlib import Path

import json
import shutil
import os
from proyecto_musica.settings import BASE_DIR

from django.utils.timezone import utc
import datetime


# TODO: implement delete user functionality
# Create your views here.


class AuthUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EditSerializer

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        serialized_data = (serializer.data).copy()
        if 'gender' in serializer.data:
            serialized_data.pop('gender')

        res = {'success' : True, 'user': serialized_data}
        return response.Response(res)

    def patch(self, request):
        jd = request.data
        id = request.user.id
        context = {}

        try:
            user_obj = User.objects.get(id=id)
        except User.DoesNotExist:
            res = {'success' : False, 'error' : "User id does not exist."}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        # check body fields
        request_keys = list(jd.keys())
        allowed_keys = [e.value for e in User_Fields]
        for key in request_keys:
            if key not in allowed_keys:
                res = {'success' : False,
                        'error' : "Wrong parameter(s) passed in request."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

        for field in List_Fields:
            field_name = field.value

            if field_name in jd:
                field_list = jd[field_name]
                res = validate_field(field_name, field_list)
                if res:
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)
                context[field_name] = field_list

        serializer = EditSerializer(user_obj, data=jd,
                                           context=context, partial=True)

        if serializer.is_valid():
            serializer.save()

            # only return fields that were modified
            serialized_data = (serializer.data).copy()
            for field in serializer.data:
                if field not in jd and field != 'gender_name':
                    serialized_data.pop(field)

            if 'gender' in jd:
                serialized_data.pop('gender')

            if 'gender' not in jd:
                serialized_data.pop('gender_name')

            res = {'success' : True, 'user': serialized_data}
            return response.Response(res, status=status.HTTP_201_CREATED)

        res = {'success' : False, 'user': serializer.errors}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)


    # deleting the use
    def delete(self, request):

        id = request.user.id
        User_Genres.objects.filter(user_id=id).delete()
        User_Skills.objects.filter(user_id=id).delete()
        User_Artists.objects.filter(user_id=id).delete()

        # deleting the pics
        pics = Images.objects.filter(user_id=id)


        for pic in pics:
            pic.image.delete()
            pic.delete()

        # deleting the videos
        vids = Videos.objects.filter(user_id=id)

        for video in vids:
            video.video.delete()
            video.delete()


        # TODO: delete its media folder
        file_location = os.path.join(BASE_DIR, 'media/videos/' + str(id))
        p = Path(file_location)
        if p.is_dir():
            shutil.rmtree(file_location, ignore_errors = False)



        # deletes image folder
        # delete its images folder
        file_location = os.path.join(BASE_DIR, 'media/photos/' + str(id))
        p = Path(file_location)

        if p.is_dir():
            shutil.rmtree(file_location, ignore_errors = False)

        #delete user
        usr = User.objects.get(id = id)
        usr.delete()






        res = {'success' : True, 'message': 'user has been deleted'}
        return response.Response(res, status=status.HTTP_201_CREATED)



class RegisterAPIView(GenericAPIView):

    serializer_class= RegisterSerializer

    def post(self, request):
        jd = request.data
        context = {}

        # check body fields
        request_keys = list(jd.keys())
        allowed_keys = [e.value for e in User_Fields]
        for key in request_keys:
            if key not in allowed_keys:
                res = {'success' : False,
                        'error' : "Wrong parameter(s) passed in request."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

        for field in List_Fields:
            field_name = field.value

            if field_name in jd:
                field_list = jd[field_name]
                res = validate_field(field_name, field_list)
                if res:
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)
                context[field_name] = field_list

        serializer = self.serializer_class(data=jd,
                                           context=context)

        if serializer.is_valid():
            serializer.save()

            serialized_data = (serializer.data).copy()
            serialized_data.pop('gender')

            res = {'success' : True, 'user': serialized_data}
            return response.Response(res, status=status.HTTP_201_CREATED)

        res = {'success' : False, 'user': serializer.errors}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)


# this used to log in the user
# response gives us the token if it is a valid login
class LoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class= LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user=authenticate(username=email, password=password)

        if user:
            serializer=self.serializer_class(user)


            response = Response(serializer.data, status.HTTP_200_OK)

            response.set_cookie(key='jwt', value=user.token, httponly=True)

            return response

            # return response.Response(serializer.data, status.HTTP_200_OK)

        return response.Response({'message': "invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)


# verifying email when creating an account
class VerifyEmail(GenericAPIView):
    def get(self, request):
        datos = {'codigo':"400",'message': "a message"}
        return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

    # this post is in charge of sending an email
    def post(self, request):
        jd = request.data
        if 'email' in jd and 'code' not in jd:
            email = jd['email']

            if User.objects.filter(email=email).count() > 0:
                datos = {'success':False,'message': "an account with that email already exists"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            # check if email exists in database
            verCodeObj = Verification.objects.filter(email=email)
            if verCodeObj.count() > 0:
                Verification.objects.filter(email=email).delete()

            code = Util.random_with_N_digits(6) # generate code
            email_body = 'Hi, this is your confirmation code. It expires in 5 minutes.\n' + str(code)
            dat = {'email_body':email_body, 'to_email':email, 'email_subject':'Verify your email'}
            Verification.objects.create(code=code, email=email)
            Util.send_email(dat)
            datos = {'success':True,'message': "confirmation code was sent"}
            return response.Response(datos, status=status.HTTP_201_CREATED)

        elif 'code' in jd and 'email' in jd:
            email = jd['email']
            code = jd['code']

            # just in case that email is already verified
            if User.objects.filter(email=email).count() > 0:
                datos = {'success':False,'message': "an account with that email is already verified"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            verificationObj = Verification.objects.get(email=email)


            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = (now - verificationObj.created_at) # converted to
            if timediff <= datetime.timedelta(minutes=5):
                if verificationObj.code == int(code):
                    datos = {'success':True,'message': "email was confirmed"}
                    return response.Response(datos, status=status.HTTP_201_CREATED)
                else:
                    datos = {'success':False,'message': "invalid code"}
                    return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)
            else:
                # this meaans time has expired
                Verification.objects.filter(email=email).delete()
                datos = {'success':False,'message': "Time has expired. Please get a new token"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

        # send code to email

# this view is used to reset the password of the user
class ForgotPassword(GenericAPIView):
    def post(self, request):
        # if code equals to code that we have saved
        # check if there is an email
        jd = request.data

        # verify that that we have enail
        if 'email' not in jd:
            # TODO add serializer
            datos = {'success':False,'error': "no email"}
            return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

        # check if the email exists in out database
        tot_users = User.objects.filter(email=jd['email']).count()

        if tot_users != 1:
            datos = {'success':False,'error': "not a valid user"}
            return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

        email = jd['email']

        verCodeObj = Verification.objects.filter(email=email)
        if verCodeObj.count() > 0:
            Verification.objects.filter(email=email).delete()


        code = Util.random_with_N_digits(6) # generate code
        email_body = 'Hi, this is your confirmation code. It expires in 5 minutes.\n' + str(code)
        dat = {'email_body':email_body, 'to_email':email, 'email_subject':'Verify your email'}
        Verification.objects.create(code=code, email=email)
        Util.send_email(dat)
        # now here we send the code to their email

        '''
        user = User.objects.get(email=jd['email'])

        # this code right here to reset the password
        token=RefreshToken.for_user(user).access_token
        '''

        datos = {'success':True,'message': 'code has been sent'}
        return response.Response(datos, status=status.HTTP_201_CREATED)

class VerifyForgotPassword(GenericAPIView):
    # this will return code that can be used to edit the password
    def get(self, request):
        datos = {'success':True,'message': "wowowowowowoowowowowow"}
        return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        jd = request.data

        if 'code' in jd and 'email' in jd:
            email = jd['email']
            code = jd['code']
            # check if a verification code has been sent
            if Verification.objects.filter(email=email).count() == 0:
                datos = {'success':False,'message': "no code has been sent"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            verificationObj = Verification.objects.get(email=email)

            if verificationObj.code != int(code):
                datos = {'success':False,'message': "invalid token"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = (now - verificationObj.created_at) # converted to
            if timediff <= datetime.timedelta(minutes=5):
                if verificationObj.code == int(code):
                    user = User.objects.get(email=jd['email'])
                    # this code right here to reset the password
                    token=RefreshToken.for_user(user).access_token

                    datos = {'success':True,'message': str(token)}
                    return response.Response(datos, status=status.HTTP_201_CREATED)
                else:
                    datos = {'success':False,'message': "invalid code"}
                    return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)
            else:
                # this meaans time has expired
                Verification.objects.filter(email=email).delete()
                datos = {'success':False,'message': "Time has expired. Please get a new token"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=jd['email'])
        # this code right here to reset the password
        token=RefreshToken.for_user(user).access_token

        datos = {'success':False,'token': str(token)}

        return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)
