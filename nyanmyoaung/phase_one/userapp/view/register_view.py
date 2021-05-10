from rest_framework.views import APIView
from userapp.serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from userapp.models import User
from userapp.constant import signup_success, signup_fail
# from django.contrib import auth


class RegisterView(APIView):
    def post(self, request):
        content = {"isSuccessful": False, "message": "Sign Up Fail"}
        try:
            serializer = RegisterSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                del data['photo_url']
                signup_success.update({'user': data})
                return Response(signup_success, status=status.HTTP_201_CREATED)
            else:
                return Response(signup_fail)
        except Exception as error:
            print("Error Message", error)
            return Response(signup_fail, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        user = User.objects.get(id=id)
        user = RegisterSerializer(user)
        return Response(user.data)
