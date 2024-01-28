from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from user_login.serializers import UserSerializer

class UserSignup(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        print(request.data)

        user = UserSerializer(data=request.data)
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

class UserProfile(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.username
        }

        return Response(data, status=status.HTTP_200_OK)

