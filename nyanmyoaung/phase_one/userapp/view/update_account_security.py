from userapp.serializers import RegisterSerializer, PhoneLoginSerializer, IdLoginSerializer,ResetPasswordSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from userapp.models import *
from django.contrib import auth
import phonenumbers
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
from userapp.id_generator import id_size
import datetime

@api_view(['POST'])
def verify_password(request,user_id):
    try:
        if request.method == 'POST':
            password = request.data['password']
            user = User.objects.get(id=user_id)
            if check_password(password,user.password):
                return Response({"password":"valid"})
            else:
                return Response({"password":"invalid"})
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def change_chit_chat_id(request,user_id):
    try:
        fail = {"chit_chat_id":"invalid"}
        if request.method == 'POST':
            new_chit_chat_id = request.data['chit_chat_id']
            if len(new_chit_chat_id) == id_size:
                user = User.objects.filter(chit_chat_id=new_chit_chat_id).exists()
                print(user)

                if not user:
                    user = User.objects.get(id=user_id)
                    profile = AccountSecurity.objects.get(user_id=user_id)
                    profile.id_changed_date = datetime.datetime.now()
                    profile.id_changeable = False
                    profile.id_changeable_date = profile.id_changed_date + datetime.timedelta(days=365)
                    profile.save()
                    user.chit_chat_id = new_chit_chat_id
                    date = profile.id_changeable_date-profile.id_changed_date
                    print("Difference:",date)
                    user.save()
                    return Response({"chit_chat_id":"valid"})
                else:
                    return Response(fail)

            else:
                return Response(fail)
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def change_password(request,user_id):
    try:
        print("here")
        if request.method == 'POST':
            old_password = request.data['old_password']
            new_password = request.data['new_password']
            user = User.objects.get(id=user_id)
            if check_password(old_password,user.password):
                user.set_password(new_password)
                user.save()
                return Response("success")
            else:
                return Response("fail")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)