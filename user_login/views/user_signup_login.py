from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from user_login.serializers import UserSerializer

class UserSignup(APIView):
    def post(self, request, format=None):
        data = {
            "user": {
                "username": request.data.get('username'),
                "password": request.data.get('password')
            }
        }

        user = UserSerializer(data=data)
        if user.is_valid(raise_exception=True):
            user.save()
            return Response({"success": "true"})


class UserLogin(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        print(request.data)
        buser = authentication.authenticate(
            username=request.data.get('username'),
            password=request.data.get('password'))
        if buser:
            token, _ = Token.objects.get_or_create(user=buser)
            return Response({"token": token.key})

        raise exceptions.AuthenticationFailed("Invalid Credentials")
