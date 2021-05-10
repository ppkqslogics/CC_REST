from rest_framework.response import Response
from rest_framework import status
from userapp.models import General
from rest_framework.decorators import api_view

@api_view(['POST'])
def update_auto_download_hd(request,user_id):
    try:
        if request.method == 'POST':
            user_general = General.objects.get(user_id=user_id)
            user_general.auto_download_hd = request.data["auto_download_hd"]
            user_general.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_auto_save_photo(request,user_id):
    try:
        if request.method == 'POST':
            user_general = General.objects.get(user_id=user_id)
            user_general.auto_save_photo = request.data["auto_save_photo"]
            user_general.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_auto_save_video(request,user_id):
    try:
        if request.method == 'POST':
            user_general = General.objects.get(user_id=user_id)
            user_general.auto_save_video = request.data["auto_save_video"]
            user_general.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_auto_play_mobile(request,user_id):
    try:
        if request.method == 'POST':
            user_general = General.objects.get(user_id=user_id)
            user_general.auto_play_mobile = request.data["auto_play_mobile"]
            user_general.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_auto_play_wifi(request,user_id):
    try:
        if request.method == 'POST':
            user_general = General.objects.get(user_id=user_id)
            user_general.auto_play_wifi = request.data["auto_play_wifi"]
            user_general.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_moments(request,user_id):
    try:
        if request.method == 'POST':
            user_general = General.objects.get(user_id=user_id)
            user_general.moments = request.data["moments"]
            user_general.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_dating(request,user_id):
    try:
        if request.method == 'POST':
            user_general = General.objects.get(user_id=user_id)
            user_general.dating = request.data["dating"]
            user_general.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_pigeon_message(request,user_id):
    try:
        if request.method == 'POST':
            user_general = General.objects.get(user_id=user_id)
            user_general.pigeon_message = request.data["pigeon_message"]
            user_general.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_sticker_gallery(request,user_id):
    try:
        if request.method == 'POST':
            user_general = General.objects.get(user_id=user_id)
            user_general.sticker_gallery = request.data["sticker_gallery"]
            user_general.save()
            return Response("success")
    except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)