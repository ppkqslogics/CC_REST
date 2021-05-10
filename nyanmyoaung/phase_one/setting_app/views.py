import datetime

import phonenumbers
from contact_app.models import Contact, Relationship
from django.contrib import auth
from django.utils import timezone
from profile_app.models import Profile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from userapp.models import User
from userapp.serializers import IdLoginSerializer, PhoneLoginSerializer
from django.contrib import auth

from setting_app.models import Privacy
from setting_app.serializers import BlockListSerializer, PrivacySerializer


class PrivacyView(APIView):

    """
    INPUT: user_id
    RESPONSE : user privacy
    SERIALIZER : -
    NOT APPLIED
    """

    def get(self, request, user_id):
        try:
            data = privacy(user_id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            user = User.objects.filter(id=user_id)
            if user.exists():
                user = user.first()
                user_privacy = Privacy(user=user)
                user_privacy.save()
                data = privacy(user_id)
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({
                    "Error": "User Doesn't Exist"
                }, status=status.HTTP_404_NOT_FOUND)


def privacy(user_id):
    user_privacy = Privacy.objects.get(user_id=user_id)
    serializer = PrivacySerializer(user_privacy)
    data = {
        'isSuccessful': True,
        'message': 'Loaded User Privacy',
        'privacy': serializer.data
    }
    return data


class UpdateReqMsgView(APIView):

    """
    INPUT : req_msg, user_id
    MODEL : Privacy
    RESPONSE : Messages
    """

    def post(self, request):
        try:
            req_msg = request.data["req_msg"]
            user_id = request.data["user_id"]
            # user_obj = User.objects.get(id=user_id)
            privacy_obj = Privacy.objects.get(user_id=user_id)
            privacy_obj.req_msg = req_msg
            privacy_obj.save()
            # serializer = PrivacySerializer(privacy_obj)
            return Response(
                {
                    'isSuccessful': True,
                    'message': 'Success'
                }
            )
        except Exception as error:
            print("PRIVACY UPDATE ERROR: ", error)
            return Response(
                {
                    "isSuccessful": False,
                    "message": 'Fail'
                }
            )


class MySetting(APIView):

    """
    INPUT : user_id
    RESPONSE : -
    **NOT FULLY FINISHED**
    """

    def get(self, request, user_id):
        try:
            user_obj = User.objects.get(id=user_id)
            privacy = user_obj.privacy.req_msg
            return Response(
                {
                    'isSuccessful': True,
                    'message': 'Successfully loaded setting',
                    'privacy': privacy
                }
            )
        except Exception as error:
            print("MY SETTING ERROR: ", error)
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Fail to load setting',
                }
            )


class ChangePasswordView(APIView):

    """
    INPUT : phone, old_password, new_password
    MODEL : User
    RESPONSE : Messages 
    URL : /change_password/
    METHOD : POST
    """

    def post(self, request):

        try:
            phone = request.data["phone"]
            password = request.data["old_password"]
            newpassword = request.data["new_password"]
            print(f'{phone} password is {password}')
            user = auth.authenticate(phone=phone, password=password)

            if not user:
                return Response({
                    'isSuccessful': False,
                    'message': 'Phone and password does not match.'
                })

            user = User.objects.get(phone=phone)
            user.set_password(newpassword)
            user.save()

            return Response({
                'isSuccessful': True,
                'message': 'Password changed successfully'
            })
        except Exception as error:
            print("CHANGE PASSWORD ERROR: ", error)
            return Response({
                'isSuccessful': False,
                'message': 'Fail to change password'
            })


class ChangeCCIDVerify(APIView):

    """
    To Verify CCID can change or not.
    INPUT : user_id \n
    RESPONSE : messages \n
    MODEL : User \n
    SERIALIZER : - \n 
    URL : /ccid_change_verify/<user_id>/ \n
    METHOD : GET
    """

    def get(self, request, user_id):
        try:
            user_obj = User.objects.get(id=user_id)
            # current_time = timezone.now()
            user_time = user_obj.ccid_updated_at
            if user_time is not None:
                diff_time = timezone.now() - user_time
                if diff_time >= datetime.timedelta(days=365):
                    pass
                else:
                    time = timezone.now() - user_time
                    duration = datetime.timedelta(days=365) - time
                    return Response({
                        "isSuccessful": False,
                        "message": "ChitChatID can't change.",
                        "time": str(duration)
                    })
            return Response({
                "isSuccessful": True,
                "message": "ChitChatID can change."
            })
        except Exception as error:
            print("CHANGE CCID ERROR: ", error)
            return Response({
                "isSuccessful": False,
                "message": "Something is occured."
            })


class ChangeChitChatIdView(APIView):

    """
    INPUT : phone, chit_chat_id\n
    RESPONSE : messages \n
    MODEL : User \n
    SERIALIZER : - \n 
    URL : /change_chitchat_id/ \n
    METHOD : POST
    """

    def post(self, request):
        try:
            user_id = request.data["user_id"]
            new_chitchatId = request.data["chit_chat_id"]
            user_obj = User.objects.filter(chit_chat_id=new_chitchatId)
            if user_obj.exists():
                return Response({
                    'isSuccessful': False,
                    'message': 'ChitChatId already exist.'
                })
            # phone = phonenumbers.parse(phone, None)
            # phone = str(phone.country_code)+str(phone.national_number)
            user = User.objects.filter(id=user_id)

            if not user:
                return Response({
                    'isSuccessful': False,
                    'message': 'Phone and password does not match.'
                })
            user = user.first()
            user.chit_chat_id = new_chitchatId
            user.ccid_updated_at = timezone.now()
            user.save()
            return Response({
                'isSuccessful': True,
                'message': 'ChitChat Id changed successfully'
            })
        except Exception:
            return Response({
                'isSuccessful': False,
                'message': 'Fail to change ChitChatId'
            })


class BlockListView(APIView):

    """
    INPUT : user_id
    RESPONSE : block_list
    MODEL : User, Contact
    SERIALIZER : BlockListSerializer
    URL : /block_list/<user_id>/
    METHOD : Get
    """

    def get(self, request, user_id):
        try:
            print("=======>", request.user.id)
            user_obj = User.objects.get(id=user_id)
            block_query = user_obj.contact.block_list.all()
            serializer = BlockListSerializer(block_query, many=True, context={
                "request": request})
            return Response({
                "isSuccessful": True,
                "message": "Successfully load block lists.",
                "block_list": serializer.data
            })
        except Exception as error:
            print("BLOCK LIST ERROR: ", error)
            return Response({
                "isSuccessful": False,
                "message": "Error occuring at block lists."
            })


class UnblockFriendView(APIView):

    """
    INPUT : user_id
    RESPONSE : Messages
    MODEL : Contact, Relationship, Profile
    SERIALIZER : -
    URL : /unblock_friend/
    METHOD : POST
    """

    def post(self, request):
        try:
            user_id = request.data['user_id']
            user_contact = Contact.objects.get(user_id=user_id)
            friend_id = request.data['friend_id']
            friend_profile = Profile.objects.get(user_id=friend_id)
            rs_obj_one = Relationship.objects.filter(
                sender=user_id, receiver=friend_id, status='block')
            rs_obj_two = Relationship.objects.filter(
                sender=friend_id, receiver=user_id, status='block')
            rs_obj = rs_obj_one or rs_obj_two
            if rs_obj.exists():
                rs_obj = rs_obj.first()
                rs_obj.delete()
                if friend_profile in user_contact.block_list.all():
                    user_contact.block_list.remove(friend_profile)
                    return Response({
                        "isSuccessful": True,
                        "message": "Unblock successful."
                    })
                else:
                    pass
            return Response({
                "isSuccessful": False,
                "message": "Failed to unblock this user",
            })
        except Exception as error:
            print("UNBLOCK ERROR: ", error)
            return Response({
                "isSuccessful": False,
                "message": "Something has occured.",
            }, status=status.HTTP_400_BAD_REQUEST)


class ChangePhoneNo(APIView):
    def post(self, request):
        try:
            phone = request.data['phone']
            phone = phonenumbers.parse(phone, None)
            phone = str(phone.country_code)+str(phone.national_number)
            user_obj = User.objects.filter(phone=phone)
            if user_obj:
                return Response({
                    "isSuccessful": False,
                    "message": "Phone number is invalid"
                })
            user = User.objects.get(id=request.data['user_id'])
            user.phone = phone
            user.save()
            return Response({
                "isSuccessful": True,
                "message": "Successfully changed phone number."
            })
        except Exception as error:
            print("CHANGE PHONE ERROR: ", error)
            return Response({
                "isSuccessful": False,
                "message": "Phone number is invalid"
            }, status=status.HTTP_400_BAD_REQUEST)


class AuthenticatePhone(APIView):   
    def post(self, request):
        try:
            content = {
                "isSuccessful": False,
                "message": "Authentication Fail"
            }
            phone = request.data['phone']
            password = request.data['password']
            user = auth.authenticate(phone=phone, password=password)
            if user:
                return Response({
                    "isSuccessful": True,
                    "message": "Authentication successful."
                })
            else:
                return Response(content)
        except Exception as error:
            print("ID VERIFY ERROR: ", error)
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccount(APIView):
    def post(self, request):
        try:
            user = User.objects.get(id=request.data['user_id'])
            user.delete()
            return Response({
                "isSuccessful":True,
                "message":"Your account is deleted."
            })
        except Exception as error:
            print("ACCOUNT CANCELLATION ERROR: ", error)
            return Response({
                "isSuccessful":False,
                "message":"Fail to delete account."
            })

class Report(APIView):
    def post(self, request):
        try:
            user = User.objects.get(id=request.data['user_id'])
            other_id = User.objects.get(id = request.data['other_id'])
            reason = request.data['reason']
            return Response({
                "isSuccessful":True,
                "message":"Successfully reported."
            })
        except Exception as error:
            print("REPORT ERROR", error)
            return Response({
                "isSuccessful":False,
                "message":"Failed to report."
            })

class Report(APIView):
    def post(self, request):
        try:
            user = User.objects.get(id=request.data['user_id'])
            other_id = User.objects.get(id = request.data['other_id'])
            reason = request.data['reason']
            return Response({
                "isSuccessful":True,
                "message":"Successfully reported."
            })
        except Exception as error:
            print("REPORT ERROR", error)
            return Response({
                "isSuccessful":False,
                "message":"Failed to report."
            })

class HelpAndFeedback(APIView):
    def post(self, request):
        try:
            user = User.objects.get(id=request.data['user_id'])
            reason = request.data['reason']
            return Response({
                "isSuccessful":True,
                "message":"Successfully sent."
            })
        except Exception as error:
            print("HelpAndFeedback", error)
            return Response({
                "isSuccessful":False,
                "message":"Failed to sent."
            })
