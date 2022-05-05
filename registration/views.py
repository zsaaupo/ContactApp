from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.utils import json
from .models import AppUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect


# Create your views here.
def sign_up(request):
    return render(request, 'sign_up.html')


def sign_in(request):
    return render(request, 'sign_in.html')


def sign_out(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('access')
    response.delete_cookie('user_name')
    return response


# APIs
class UserSignIn(generics.ListAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        result = {}
        try:
            data = json.loads(request.body)
            print(data)
            if 'email' not in data or data['email']=='':
                result['message']="Email can not be null."
                result['Error']="Email"
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            if 'password' not in data or data['password'] == '':
                result['message'] = "Password can not be null."
                result['Error'] = "Password"
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=data['email']).first()
            if not user:
                result = {
                    'message': 'Please create a account'
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            elif not user.is_active:
                result = {
                    'message': 'Please activate your account'
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                if not check_password(data['password'], user.password):
                    result['message'] = "Invalid credentials"
                    return Response(result, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    app_user = AppUser.objects.filter(user=user).first()
                    refresh_token = RefreshToken.for_user(user)
                    data = {
                        'user_name': user.username,
                        'slug': app_user.slug,
                        'access': str(refresh_token.access_token),
                        'token': str(refresh_token),
                        'status': status.HTTP_200_OK
                    }
                    return Response(data)
        except Exception as e:
            result = {}
            result['status'] = status.HTTP_400_BAD_REQUEST
            result['message'] = str(e)
            return Response(result)


class UserSignUp(generics.CreateAPIView):
    permission_classes = []

    def post(self, request):
        result = {}
        try:
            data = request.data
            # data = json.loads(request.body)

            if 'full_name' not in data or data['full_name'] == '':
                return Response("Full name can not be null.")
            if 'email' not in data or data['email'] == '':
                return Response("Email can not be null.")
            if 'password' not in data or data['password'] == '':
                return Response("Password can not be null.")

            user = User.objects.filter(email=data['email']).first()

            if user:
                return Response("You have account")

            if not user:
                user = User()
                user.username = data['full_name']
                user.first_name = data['full_name']
                user.email = data['email']
                user.password = make_password(data['password'])
                user.save()
                app_user = AppUser()
                app_user.user = user
                app_user.full_name = data['full_name']
                app_user.email = data['email']
                app_user.save()

                result = {
                    'status': status.HTTP_200_OK,
                    'message': "successfully created.......!"
                }
                return Response(result)

        except Exception as ex:
            return Response(str(ex))

