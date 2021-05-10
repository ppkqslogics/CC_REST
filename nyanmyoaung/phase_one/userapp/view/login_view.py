from rest_framework.views import APIView
from userapp.serializers import PhoneLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from userapp.models import User
from userapp.constant import login_success, login_fail

class PhoneLoginView(APIView):    
    def post(self, request):
        try:
            serializer = PhoneLoginSerializer(data=request.data,context={"request": request})
            if serializer.is_valid():
                data = serializer.data['user']
                del data['photo_url']
                login_success.update({'user':data})
                return Response(login_success,status=status.HTTP_200_OK)
            else:
                return Response(login_fail)
        except Exception as error:
            print("Login Error: ", error)
            return Response(login_fail, status=status.HTTP_404_NOT_FOUND)

class IdLoginView(APIView):
    def post(self, request):
        try:
            chit_chat_id = request.data['chit_chat_id']
            password = request.data['password']
            phone = User.objects.get(chit_chat_id=chit_chat_id)
            serializer = PhoneLoginSerializer(data={'phone':'+'+str(phone.phone),'password':password},context={"request": request})
            if serializer.is_valid():
                data = serializer.data['user']
                del data['photo_url']
                login_success.update({'user':data})
                return Response(login_success,status=status.HTTP_200_OK)
            else:
                return Response(login_fail)
        except Exception as error:
            print("Login Error: ", error)
            return Response(login_fail)

class PhoneVerifyView(APIView):
    def post(self,request):
        try:
            phone = phonenumbers.parse(request.data['phone'], None)
            phone = str(phone.country_code)+str(phone.national_number)
            verify_phone = User.objects.get(phone=phone)
            return Response({'isSuccessful':True,'message':'Phone Number is Valid','phone':'+'+str(verify_phone.phone)})
        except Exception:
            return Response({'isSuccessful':False,'message':'Phone Number is Invalid'})

class IdVerifyView(APIView):
    def post(self,request):
        try:
            verify_phone = User.objects.get(chit_chat_id=request.data['chit_chat_id'])
            return Response({'isSuccessful':True,'message':'ID is valid','phone':'+'+str(verify_phone.phone)})
        except Exception:
            return Response({'isSuccessful':False,'message':'ID is Invalid'})