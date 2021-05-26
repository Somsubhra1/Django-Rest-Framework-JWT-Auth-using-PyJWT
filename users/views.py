from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from .models import User
import jwt
import datetime
import os

# Create your views here.

JWT_SECRET = os.environ.get('JWT_SECRET')


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'success': True,
            'token': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise NotAuthenticated('Unauthenticated')

        try:
            payload = jwt.decode(token, JWT_SECRET, ['HS256'])
        except jwt.ExpiredSignatureError:
            raise NotAuthenticated('Unauthenticated')

        user = User.objects.get(id=payload['id'])

        serializer = UserSerializer(user)

        return Response(serializer.data)


class Logout(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')

        response.data = {
            'success': True
        }

        return response
