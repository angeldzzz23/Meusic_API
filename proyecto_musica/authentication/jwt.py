import jwt
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from authentication.models import User

from rest_framework import exceptions
import jwt

from django.conf import settings

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
#


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = get_authorization_header(request)

        if not auth_header:
            return None

        auth_data = auth_header.decode('utf-8')

        auth_token = auth_data.split(" ")

        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed('Token not valid')

        token = auth_token[1]

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")
            print("payloaddddd")
            print(payload)

            id_user = ""

            if "id" not in payload:
                print("hehe")
                id_user = payload['user_id']
            else:
                print("hahah")
                id_user = payload['id']


            user = User.objects.get(id=id_user
                                    )
            return (user, token)

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is expired, login again')

        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is invalid,')

        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(
                'No such user')

        return super().authenticate(request)
