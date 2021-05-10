from rest_framework.response import Response
from rest_framework import status
from userapp.models import User, Privacy
from rest_framework.decorators import api_view

@api_view(['POST'])
def update_friend_request(request,user_id):
    try:
        if request.method == 'POST':
            user_privacy = Privacy.objects.get(user_id=user_id)
            user_privacy.require_friend_request = request.data["require_firend_request"]
            user_privacy.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_recommend_me(request,user_id):
    try:
        if request.method == 'POST':
            user_privacy = Privacy.objects.get(user_id=user_id)
            user_privacy.recommend_me = request.data["recommend_me"]
            user_privacy.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_visible_to(request,user_id):
    try:
        if request.method == 'POST':
            user_privacy = Privacy.objects.get(user_id=user_id)
            user_privacy.visible_to = request.data["visible"]
            user_privacy.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_visible_time(request,user_id):
    try:
        if request.method == 'POST':
            user_privacy = Privacy.objects.get(user_id=user_id)
            user_privacy.visible_time = request.data["visible_time"]
            user_privacy.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

