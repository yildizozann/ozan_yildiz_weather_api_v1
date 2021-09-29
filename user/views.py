from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.authtoken.models import Token
import json
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
# Create your views here.
@api_view(["POST"])
@permission_classes([AllowAny])
def Register_Users(request):
#"""This endpoint allows for creation of a user"""

    try:
        data = {}
        serializer = RegistrationSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            data["message"] = "user registered successfully"
            data["email"] = account.Email_Address
            data["username"] = account.name
            data["token"] = token
            data["User_id"] = account.id

        else:
            data = serializer.errors

        return Response(data)
    except IntegrityError as e:
        account=User.objects.get(username='')
        account.delete()
        raise ValidationError({"400": f'{str(e)}'})

    except KeyError as e:
        print(e)
        raise ValidationError({"400": f'Field {str(e)} missing'})



@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
#"""This endpoint allows for login of a user"""


        data = {}
        reqBody = json.loads(request.body)
        email1 = reqBody['Email_Address']
        print(email1)
        password = reqBody['password']
        try:

            Account = Users.objects.get(Email_Address=email1)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=Account)[0].key
        print(token)
        if not Account.check_password(password) and password != Account.password :
            raise ValidationError({"message": "Incorrect Login credentials"})

        if Account:
            if Account.is_active:
                print(request.user)
                login(request, Account)
                data["Message"] = "user succesfully logged in"
                data["Email_address"] = Account.Email_Address
                data["User_id"] = Account.id

                Res = {"data": data, "token": token}

                return Response(Res)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})
#"""This endpoint allows for logout of a user"""
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):


    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')

#"""This endpoint allows users to view, uptade and delete their information"""
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])

def User_info(request, pk):

    try: 
        try_user = Users.objects.get(id=pk) 
    except Users.DoesNotExist: 
        return Response({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET' :

        user = request.user
        user2 = Users.objects.get(id=pk)
        
        if user.id == user2.id:
            serializer = UsersInfoSerializer(user2, many=False)
            return Response(serializer.data)
        else:
            error = {
                'Error': 'You are not authorized to view other users information'
            }
            return Response(error)
    elif request.method == 'PUT' :
        
        user = request.user
        user2 = Users.objects.get(id=pk)
        
        if user.id == user2.id:
            serializer = RegistrationSerializer(request.user, data=request.data, partial=True)
            
            serializer.is_valid()
            serializer.save()
            return Response({"message": 'User updated succesfully!'})

        else:
            error = {
                'Error': 'You are not authorized to update other users information'
            }
            return Response(error)

    elif request.method == 'DELETE' :

        user = request.user
        user2 = Users.objects.get(id=pk)
        
        if user.id == user2.id:
            try_user.delete()
            return Response({"message": 'User deleted succesfully!'})
        else:
            error = {
                'Error': 'You are not authorized to delete other users information'
            }
            return Response(error)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weatherInformationId(request, pk):
    alldata = WeatherClass.objects.get(id = pk)
    serializer = WeatherClassSerializer(alldata, many =False)   # serializing data
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weatherInformationLocation(request, pk):
    alldata = WeatherClass.objects.filter(location = pk)
    serializer = WeatherClassSerializer(alldata, many =True)   # serializing data
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weatherInformationCondition(request, pk):
    alldata = WeatherClass.objects.filter(condition = pk)
    serializer = WeatherClassSerializer(alldata, many =True)   # serializing data
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weatherInformationAverage(request, pk):
    alldata = WeatherClass.objects.filter(average = pk)
    serializer = WeatherClassSerializer(alldata, many =True)   # serializing data
    return Response(serializer.data)