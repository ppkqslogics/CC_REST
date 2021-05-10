from rest_framework.response import Response
from rest_framework import status
from userapp.models import Notifications
from rest_framework.decorators import api_view
import datetime

@api_view(['POST'])
def update_msg_noti(request,user_id):
    try:
        if request.method == 'POST':
            user_noti = Notifications.objects.get(user_id=user_id)
            user_noti.msg_noti = request.data["msg_noti"]
            user_noti.updated_at = datetime.datetime.now()
            user_noti.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_dating_noti(request,user_id):
    try:
        if request.method == 'POST':
            user_noti = Notifications.objects.get(user_id=user_id)
            user_noti.dating_noti = request.data["dating_noti"]
            user_noti.updated_at = datetime.datetime.now()
            user_noti.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_secret_msg_noti(request,user_id):
    try:
        if request.method == 'POST':
            user_noti = Notifications.objects.get(user_id=user_id)
            user_noti.secret_msg_noti = request.data["secret_msg_noti"]
            user_noti.updated_at = datetime.datetime.now()
            user_noti.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_call_noti(request,user_id):
    try:
        if request.method == 'POST':
            user_noti = Notifications.objects.get(user_id=user_id)
            user_noti.call_noti = request.data["call_noti"]
            user_noti.updated_at = datetime.datetime.now()
            user_noti.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_private_noti(request,user_id):
    try:
        if request.method == 'POST':
            user_noti = Notifications.objects.get(user_id=user_id)
            user_noti.private_noti = request.data["private_noti"]
            user_noti.updated_at = datetime.datetime.now()
            user_noti.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)
