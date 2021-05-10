import datetime
import os
from io import BytesIO

import qrcode
from django.core.files import File
from django.utils import timezone
from PIL import Image
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from userapp.models import User
from userapp.serializers import img_compress
from rest_framework.permissions import IsAuthenticated
from .models import Profile, make_qr_code
from .serializers import UserProfileSerializer
from rest_framework.decorators import permission_classes

# Create your views here.
class UserProfileView(APIView):

    """
    View for user profile
    INPUT : user_id \n
    RESPONSE : profile data \n
    MODEL : Profile \n
    SERIALIZER : UserProfileSerializer \n 
    URL : /profile/<user_id>/ \n
    METHOD : GET
    """
    permission_classes = [IsAuthenticated,]
    def get(self, request, user_id):
        try:
            self_profile = Profile.objects.get(user_id=user_id)
            serializer = UserProfileSerializer(
                self_profile, context={"request": request})
            return Response({
                'isSuccessful': True,
                'message': 'Profile Successfully Loaded',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as error:
            print("UserProfile Errror:", error)
            return Response({
                'isSuccessful': False,
                'message': 'Failed to Load Profile'
            })


class FriendProfileView(APIView):

    """
    **NOT APPLIED**
    INPUT : user_id \n
    RESPONSE : friend profile \n
    MODEL : Profile \n
    SERIALIZER : UserProfileSerializer\n 
    URL : \n
    METHOD : 
    """
    permission_classes = [IsAuthenticated,]
    def get(self, request, user_id):
        try:
            profile = Profile.objects.get(user_id=user_id)
            serializer = UserProfileSerializer(profile)
            friend_profile = {}
            friend_profile.update(serializer.data['user'])
            friend_profile.update(serializer.data)
            del friend_profile['user']
            return Response(friend_profile, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"Error": str(error)}, status=status.HTTP_404_NOT_FOUND)


class StrangerProfileView(APIView):
    '''
    **NOT APPLIED**
    Stranger Profile View Method \n
    Input : friend_profile_id \n
    Serializer : ProfileSerializer \n
    Output : Serialized Stranger Profile Data \n
    Response : Message + serialized data \n
    Note: **Need to Confirm Responser"
    '''
    permission_classes = [IsAuthenticated,]
    def get(self, request, user_id):
        try:
            profile = Profile.objects.get(user_id=user_id)
            serializer = UserProfileSerializer(profile)
            stranger_profile = {}
            stranger_profile.update(serializer.data['user'])
            stranger_profile.update(serializer.data)
            del stranger_profile['user']
            return Response(stranger_profile, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"Error": str(error)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def update_cover_photo(request):
    try:
        if request.method == 'POST':
            user_profile = Profile.objects.get(user_id=request.data['user_id'])
            photo = request.data['cover_photo']
            new_image = img_compress(photo)
            user_profile.cover_photo = new_image
            user_profile.update_at = timezone.now()
            user_profile.save()
            serializer = UserProfileSerializer(
                user_profile, context={"request": request})
            return Response({
                'isSuccessful': True,
                'message': 'Successfuly changed cover photo',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
    except Exception as error:
        print("CHANGE COVER PHOTO ERROR: ", error)
        return Response({
            'isSuccessful': False,
            'message': 'Failed to change cover photo'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def update_name(request):
    try:
        if request.method == 'POST':
            user = User.objects.get(id=request.data['user_id'])
            user.name = request.data['name']
            user.update_at = datetime.datetime.now()
            user.profile.updated_at = timezone.now()
            user.save()
            serializer = UserProfileSerializer(
                user.profile, context={"request": request})
            return Response({
                'isSuccessful': True,
                'message': 'Successfuly changed name',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
    except Exception as error:
        print("CHANGE NAME ERROR: ", error)
        return Response({
            'isSuccessful': False,
            'message': 'Failed to change name'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def update_photo(request):
    try:
        if request.method == 'POST':
            user = User.objects.get(id=request.data['user_id'])
            photo = request.data['photo']
            new_photo = img_compress(photo)
            user.photo = new_photo
            os.remove(user.profile.qr_img.path)
            img_io, fname, img = make_qr_code(profile_pic=user.photo, user_ph=user.phone, user_cc_id=user.chit_chat_id)
            img.save(img_io, "PNG")
            new_qr_img = File(img_io, name=fname)
            user.profile.qr_img = new_qr_img
            user.profile.save()
            user.update_at = timezone.now()
            user.profile.updated_at = timezone.now()
            user.save()
            serializer = UserProfileSerializer(
                user.profile, context={"request": request})
            return Response({
                'isSuccessful': True,
                'message': 'Successfuly changed photo',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
    except Exception as error:
        print("CHANGE PHOTO ERRORS: ", error)
        return Response({
            'isSuccessful': False,
            'message': 'Failed to change photo'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def update_region(request):
    try:
        user = User.objects.get(id=request.data['user_id'])
        user.region = request.data['region']
        user.update_at = timezone.now()
        user.profile.updated_at = timezone.now()
        user.save()
        serializer = UserProfileSerializer(
            user.profile, context={"request": request})
        return Response({
            'isSuccessful': True,
            'message': 'Successfuly changed region',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as error:
        print("CHANGE REGION ERROR: ", error)
        return Response({
            'isSuccessful': False,
            'message': 'Failed to change region'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def update_birthday(request):
    try:
        user_profile = Profile.objects.get(user_id=request.data['user_id'])
        my_date = datetime.datetime.strptime(
            request.data['birthday'], "%d/%m/%Y")
        user_profile.birthday = my_date.date()
        user_profile.update_at = timezone.now()
        user_profile.save()
        serializer = UserProfileSerializer(
            user_profile, context={"request": request})
        return Response({
            'isSuccessful': True,
            'message': 'Successfuly changed birth date',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as error:
        print("CHANGE BIRTHDAY ERROR: ", error)
        return Response({
            'isSuccessful': False,
            'message': 'Failed to change birth date'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def update_gender(request):
    try:
        user = User.objects.get(id=request.data['user_id'])
        user.profile.gender = request.data['gender']
        user.profile.updated_at = timezone.now()
        user.profile.save()
        serializer = UserProfileSerializer(
            user.profile, context={"request": request})
        return Response({
            'isSuccessful': True,
            'message': 'Successfuly changed gender',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as error:
        print("CHANGE gender ERROR: ", error)
        return Response({
            'isSuccessful': False,
            'message': 'Failed to change gender'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def testapi(request):
    try:
        if request.method == 'POST':
            data = request.data
            for a in data['img']:
                print("DATA", a)
            return Response("success")
    except Exception as error:
        return Response({"Error": str(error)}, status=status.HTTP_404_NOT_FOUND)
