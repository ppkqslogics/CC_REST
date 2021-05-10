from rest_framework.views import APIView
from userapp.serializers import *
from rest_framework.response import Response
from rest_framework import status
from userapp.models import *
from profile_app.models import Profile
from profile_app.serializers import UserProfileSerializer
from django.contrib import auth
#from rest_framework.permissions import IsAuthenticated
import phonenumbers
import datetime
from django.http import HttpResponse
from userapp.id_generator import otp_generator
from user.settings import OTP_TOKEN, OTP_URL
import requests
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework import authentication
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

def welcome_page(request):
    return HttpResponse("<h1>Welcome To ChitChat API Service</h1>")


class RegisterView(APIView):

    """
    CREATING NEW ACCOUNT
    INPUT : User Model Input \n
    RESPONSE : Profile Data \n
    MODEL : User, Profile \n
    SERIALIZER : UserProfileSerializer \n 
    URL : /register/ \n
    METHOD : POST
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permissions = [permissions.AllowAny,]
    serializer_class = RegisterSerializer

    def post(self, request):
        content = {"isSuccessful": False, "message": "Sign Up Fail"}
        try:
            user = request.data
            print(request)
            serializer = self.serializer_class(
                data=user, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                profile_obj = Profile.objects.get(
                    user_id=serializer.data['id'])
                profile_serializer = UserProfileSerializer(
                    profile_obj, context={"request": request})
                login(request, profile_obj.user)
                content = {"isSuccessful": True,
                           "message": "Sign Up Successfull", 
                           "user": profile_serializer.data,
                           "token": profile_obj.user.tokens()
                           }
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                return Response(content)
        except Exception as error:
            print("REGISTRAION ERROR: ", str(error))
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    """ def get(self, request, id):
        user = User.objects.get(id=id)
        user = RegisterSerializer(user)
        return Response(user.data) """


class RegisterPhoneVerificationView(APIView):

    """
    Phone Vrification at Registraiton
    INPUT : phone \n
    RESPONSE : Messages \n
    MODEL : User \n
    SERIALIZER : - \n 
    URL : /register_verification/ \n
    METHOD : POST
    """

    def post(self, request):
        try:
            phone = request.data['phone']
            phone = phonenumbers.parse(phone, None)
            phone = str(phone.country_code) + str(phone.national_number)
            user_obj = User.objects.filter(phone=phone)
            if user_obj.exists():
                return Response(
                    {
                        'isSuccessful': False,
                        'message': 'Phone number is already exist.'
                    }
                )
            else:
                return Response(
                    {
                        'isSuccessful': True,
                        'message': 'Phone number is available.'
                    }
                )
        except Exception as error:
            print("REGISTER PHONE VERIFICATION ERROR", error)
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Fail to verify phone.'
                }
            )


class PhoneLoginView(APIView):

    """
    Login with Phone
    INPUT : phone, password\n
    RESPONSE : messages\n
    MODEL : - \n
    SERIALIZER : - \n 
    URL : /phone_login/ \n
    METHOD : POST
    """

    def post(self, request):
        content = {
            "isSuccessful": False,
            "message": "Invalid Phone Number or Password"
        }
        try:
            serializer = PhoneLoginSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                data = serializer.data['user']
                user = User.objects.get(id=data['id'])
                login(request, user)
                # print(user.tokens)
                content = {
                    "isSuccessful": True,
                    "message": "Login Successfull",
                    "user": data,
                    "token": user.tokens()
                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response(content)
        except Exception as error:
            print(str(error))
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class IdLoginView(APIView):

    """
    INPUT : ccid, password\n
    RESPONSE : messages\n
    MODEL : User \n
    SERIALIZER : PhoneLoginSerializer \n 
    URL : /id_login/ \n
    METHOD : POST
    """

    def post(self, request):
        content = {
            "isSuccessful": False,
            "message": "Invalid Id or Password"
        }
        try:
            chit_chat_id = request.data['chit_chat_id']
            password = request.data['password']
            phone = User.objects.get(chit_chat_id=chit_chat_id)
            serializer = PhoneLoginSerializer(data={
                'phone': '+'+str(phone.phone),
                'password': password
                },
                context={
                    "request": request
            })
            if serializer.is_valid():
                data = serializer.data['user']
                user = User.objects.get(id=data['id'])
                login(request, user)
                content = {
                    "isSuccessful": True,
                    "message": "Login Successfull",
                    "user": data,
                    "token": user.tokens()
                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response(content)
        except Exception as error:
            print("ID LOGIN ERROR: ", error)
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class PhoneVerifyView(APIView):

    """
    Phone Validation
    INPUT : phone \n
    RESPONSE : Messages \n
    MODEL : User \n
    SERIALIZER : - \n 
    URL : /verify_phone/ \n
    METHOD : POST
    """

    def post(self, request):
        try:
            phone = phonenumbers.parse(request.data['phone'], None)
            phone = str(phone.country_code)+str(phone.national_number)
            verify_phone = User.objects.filter(phone=phone)
            if verify_phone.exists():
                verify_phone = verify_phone.first()
                return Response(
                    {
                        'isSuccessful': True,
                        'message': 'Phone Number is Valid',
                        'phone': '+'+str(verify_phone.phone)
                    }
                )
            else:
                return Response(
                    {
                        'isSuccessful': False,
                        'message': 'Phone Number is Invalid'
                    }
                )
        except Exception as error:
            print("PHONE VERIFY ERROR: ", error)
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Phone Number is Invalid'
                }
            )


class IdVerifyView(APIView):

    """
    ID Validation
    INPUT : ccid \n
    RESPONSE : Messages \n
    MODEL : User \n
    SERIALIZER : - \n 
    URL : /verify_id/ \n
    METHOD : POST
    """

    def post(self, request):
        try:
            fail_content = {
                'isSuccessful': False,
                'message': 'ID is Invalid'
            }
            verify_id = User.objects.filter(
                chit_chat_id=request.data['chit_chat_id'])
            if verify_id.exists():
                verify_id = verify_id.first()
                return Response(
                    {
                        'isSuccessful': True,
                        'message': 'ID is valid',
                        'phone': '+'+str(verify_id.phone)
                    }
                )
            else:
                return Response(fail_content)
        except Exception as error:
            print("ID VERIFY ERROR: ", error)
            return Response(fail_content)


class ForgotPasswordPhoneView(APIView):

    """
    INPUT : phone, password\n
    RESPONSE : messages \n
    MODEL : User \n
    SERIALIZER : -\n 
    URL : /forgot_password_phone/ \n
    METHOD : POST
    """

    def post(self, request):
        try:
            phone = request.data["phone"]
            password = request.data["password"]
            phone = phonenumbers.parse(phone, None)
            phone = str(phone.country_code)+str(phone.national_number)
            user = User.objects.get(phone=phone)
            user.set_password(password)
            user.save()
            return Response(
                {
                    'isSuccessful': True,
                    'message': 'Password changed successfully'
                }
            )
        except Exception:
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Fail to change password'
                }
            )


class ForgotPasswordIdView(APIView):

    """
    INPUT : ccid, password\n
    RESPONSE : messages \n
    MODEL : User \n
    SERIALIZER : -\n 
    URL : /forgot_password_id/ \n
    METHOD : POST
    """

    def post(self, request):
        try:
            chit_chat_id = request.data["chit_chat_id"]
            password = request.data["password"]
            user = User.objects.get(chit_chat_id=chit_chat_id)
            user.set_password(password)
            user.save()
            return Response(
                {
                    'isSuccessful': True,
                    'message': 'Password changed successfully'
                }
            )
        except Exception:
            return Response(
                {
                    'isSuccessful': False,
                    'change_password': 'Fail to change password'
                }
            )


class ValidateSendOTP(APIView):
    """
    OTP Sender
    **NOT APPLIED**
    """

    def post(self, request):
        try:
            phone = request.data["phone"]
            phone = phonenumbers.parse(phone, None)
            phone = str(phone.country_code) + str(phone.national_number)
            fail_otp = {
                'isSuccessful': False,
                'message': 'Fail to sent otp'
            }
            if User.objects.filter(phone=phone).exists():
                return Response(
                    {
                        'isSuccessful': False,
                        'message': 'Phone number already exist'
                    }
                )
            else:
                key = otp_generator()
                if key:
                    old_number = PhoneOTP.objects.filter(phone=phone)
                    if old_number.exists():
                        old_number = old_number.first()
                        counts = old_number.counts
                        if counts > 4:
                            return Response(
                                {
                                    'isSuccessful': False,
                                    'message': 'Otp limit exceeded. Please try again later.'
                                }
                            )
                        else:
                            response = sendOTP(phone, key)
                            old_number.otp = key
                            old_number.counts = counts + 1
                            old_number.save()
                            return Response({
                                'isSuccessful': True,
                                'message': old_number.otp,
                                'count': old_number.counts
                            })
                    else:
                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=key,
                        )
                        response = sendOTP(phone, key)
                        if response['status'] == 'true':
                            return Response({
                                'isSuccessful': True,
                                'message': 'Successfully sent OTP',
                            })
                        else:
                            return Response(fail_otp)
                else:
                    return Response(fail_otp)
        except Exception as error:
            print("OTP ERROR: ", error)
            return Response(fail_otp)


def sendOTP(phone, key):
    phone = str('+')+str(phone)
    headers = {"Authorization": "Bearer " + OTP_TOKEN}
    message = f"Your activation code for Chit Chat is {key}"
    data = {
        "to": phone,
        "message": message,
        "sender": "Chit Chat"
    }
    response = requests.post(OTP_URL, headers=headers, json=data)
    return response.json()

# class OTPVerification(APIView):
class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response({
            "isSuccessful":True,
            "message":"Logout success"
            })

class AnotherDevice(APIView):
    def get(self, request):
        return Response({
            "isSuccessful":False,
            "message":"Another device is login."
            },status=status.HTTP_401_UNAUTHORIZED)

class RefreshToken(APIView):
    def post(self, request):
        try:
            print(request.data['refresh'])
            serializer = RefreshTokenSerializer(data={"refresh":request.data['refresh']})
            serializer.is_valid() 
            print(serializer) 
            print(serializer.data)  
            return Response({
                "isSuccessful":True,
                "message":"Token valid",
                "tokens":serializer.data
            })
        except Exception as error:
            print("REFRESH TOKEN ERROR: ", error)
            return Response({
                "isSuccessful":False,
                "message":"Invalid token"
            })

