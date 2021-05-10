from userapp.serializers import RegisterSerializer, PhoneLoginSerializer, IdLoginSerializer,ResetPasswordSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from userapp.models import *
from django.contrib import auth
import phonenumbers
from rest_framework.decorators import api_view

@api_view(['POST'])
def update_cover_photo(request,user_id):
    try:
        if request.method == 'POST':
            photo = UserProfile.objects.get(user_id=user_id)
            print(request.data['cover_photo'])
            photo.cover_photo = request.data["cover_photo"]
            photo.save()
            return Response("success")
    except Exception as error:
        return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_name(request,user_id):
    try:
        if request.method == 'POST':
            name = User.objects.get(id=user_id)
            name.name = request.data['name']
            name.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_photo(request,user_id):
    try:
        if request.method == 'POST':
            photo = User.objects.get(id=user_id)
            photo.photo = request.data['photo']
            photo.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_region(request,user_id):
    try:
        if request.method == 'POST':
            region = User.objects.get(id=user_id)
            region.region = request.data['region']
            region.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_rank(request,user_id):
    try:
        if request.method == 'POST':
            rank = UserProfile.objects.get(id=user_id)
            rank.rank = request.data['rank']
            rank.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_birthday(request,user_id):
    try:
        if request.method == 'POST':
            birthday = UserProfile.objects.get(id=user_id)
            birthday.birthday = request.data['birthday']
            birthday.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)


