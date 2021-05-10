from rest_framework.views import APIView
from userapp.serializers import AccountSecuritySerializer, PrivacySerializer, GeneralSerializer
from rest_framework.response import Response
from rest_framework import status
from userapp.models import AccountSecurity, Privacy, General 

class AccountSecurityView(APIView):
    def get(self,request,user_id):
        try:
            data=security(user_id)
            print(data)
            return Response(data,status=status.HTTP_200_OK)
        except Exception:
            user = User.objects.filter(id=user_id).exists()
            if user:
                user = User.objects.get(id=user_id)
                account_security = AccountSecurity(user=user)
                account_security.save()
                data=security(user_id)
                return Response(data,status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"Error":"User Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)

def security(user_id):
    account_security = AccountSecurity.objects.get(user_id=user_id)
    today = datetime.datetime.now()
    date_time_obj = datetime.datetime.strptime(account_security.id_changeable_date.strftime("%Y-%m-%d"), '%Y-%m-%d')
    difference = date_time_obj - today
    try:
        if difference.days <= 0:
            account_security.id_changeable = True
            account_security.save()
        else:
            print("there")
    except Exception:
        pass
    serializer = AccountSecuritySerializer(account_security)
    data = {"chit_chat_id":serializer.data['user']['chit_chat_id']}
    data.update(serializer.data)
    del data['user']
    return data

class AccountCancellationView(APIView):
    def post(self,request,user_id):
        try:
            data = request.data['account_cancellation']
            if data:
                user = User.objects.get(id=user_id)
                user.delete()
                return Response({"account":"delete"})
            else:
                pass
        except Exception as error:
            return Response({"Error":str(error)},status=status.HTTP_404_NOT_FOUND)

class PrivacyView(APIView):
    def get(self,request,user_id):
        try:
            data = privacy(user_id)
            return Response(data,status=status.HTTP_200_OK)
        except:
            user = User.objects.filter(id=user_id).exists()
            if user:
                user = User.objects.get(id=user_id)
                user_privacy = Privacy(user=user)
                user_privacy.save()
                data = privacy(user_id)
                return Response(data,status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"Error":"User Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)

def privacy(user_id):
    user_privacy = Privacy.objects.get(user_id=user_id)
    serializer = PrivacySerializer(user_privacy)
    return serializer.data

class GeneralView(APIView):
    def get(self,request,user_id):
        try:
            data = general(user_id)
            return Response(data,status=status.HTTP_200_OK)
        except Exception:
            user = User.objects.filter(id=user_id).exists()
            if user:
                user = User.objects.get(id=user_id)
                user_general = General(user=user)
                user_general.save()
                data = general(user_id)
                return Response(data,status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"Error":"User Doesn't Exist"},status=status.HTTP_404_NOT_FOUND)

def general(user_id):
    user_general = General.objects.get(user_id=user_id)
    serializer = GeneralSerializer(user_general)
    return serializer.data