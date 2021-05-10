""" from rest_framework.views import APIView
from userapp.serializers import RelationshipSerializer, ContactUploadSerializer 
from rest_framework.response import Response
from rest_framework import status
from userapp.models import User, UserProfile, Relationship, Contact
import phonenumbers

# Friend Request Sent
class FriendRequestView(APIView):
    def post(self,request):
        try:
            request_data = request.data
            print(request_data)
            serializer = RelationshipSerializer(data={'sender':request_data['sender'],'receiver':request.data['receiver'],'message':request.data['message'],'status':'send'})
            if serializer.is_valid():
                serializer.save()
            return Response({"isSuccess":True,'message':'Friend Request Successfully Sent','data':serializer.data})
        except Exception:
            return Response({"isSuccess":False,'message':'Friend Request Fail to Send'})

# Friend Request Receive List
class ReceiverView(APIView):
    def get(self,request,user_id):
        try:
            requested_user = Relationship.objects.filter(receiver=user_id, status="send")
            requested_data = []
            for request_data in requested_user:
                serializer = RegisterSerializer(request_data.sender.user,context={"request": request})
                request_message = {'request_message':request_data.message}
                request_message.update(serializer.data)
                del request_message['photo_url']
                requested_data.append(request_message)
            if requested_data == []:
                return Response({'isSuccessful':False,'message':'No New Friends Request'})
            else:
                content = {'isSuccessful':True,'message':'Successfully Loaded Friends Request'}
                content.update({'request_friend':requested_data})
                return Response(content)
        except Exception:
            return Response({'isSuccessful':False,'message':'Failed to Load Friends Request'})

# Friend Request Sent List
class SenderView(APIView):
    def get(self,request,user_id):
        user = Relationship.objects.filter(sender=user_id, status="send")
        user = RelationshipSerializer(user, many=True)
        return Response(user.data)

# To Confirm Friend Request
class ConfirmFriendView(APIView):
    def post(self,request):
        sender = request.data['sender']
        receiver = request.data['receiver']
        nickname = request.data['nickname']
        confirm = Relationship.objects.filter(sender=sender, receiver=receiver).update(status='confirmed')
        status = Relationship.objects.get(sender=sender, receiver=receiver)
        status = RelationshipSerializer(status)
        if status.data['status']=='confirmed':
            sender_contact = Contact.objects.get(user_id=sender)
            sender_profile = UserProfile.objects.get(user_id=sender)
            receiver_contact = Contact.objects.get(user_id=receiver)
            receiver_profile = UserProfile.objects.get(user_id=receiver)
            sender_contact.friends.add(receiver_profile)
            receiver_contact.friends.add(sender_profile)
            sender_contact.save()
            receiver_contact.save()
            return Response({'isSuccessful':True,'message':'You are now friend'})
        else:
            return Response({'isSuccessful':False,'message':'Friend Request Failed to Confrim'})

# Add New Friend to Tag
class TagsView(APIView):
    def post(self,request):
        user_id = request.data['user_id']
        tag = request.data['tag']
        splitted_tag = list(tag.split(","))
        tag_name = request.data['tag_name']
        serializer = TagsSerializer(data={'user':user_id,'tag_name':tag_name,'tag':splitted_tag})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# Finding the User with ID or Phone (+95 or 09 or 9)
class FindFriendView(APIView):
    def post(self,request):
        try:
            user = User.objects.get(id=request.data['user_id'])
            identifier = request.data['find_friend']
            if identifier[0] == '+':
                country_code = None
                phone = phoneparser(identifier,country_code)
                contact_data = contact_upload(phone,user,request)
                return Response({'isSuccessful':True,'message':'Successfully find user','user':contact_data})
            elif identifier.isdigit():
                country_code = user.get_country_code()
                phone = phoneparser(identifier,country_code)
                contact_data = contact_upload(phone,user,request)
                return Response({'isSuccessful':True,'message':'Successfully find user','user':contact_data})
            else:
                if User.objects.filter(chit_chat_id=identifier).exists():
                    friend = User.objects.get(chit_chat_id=identifier)
                    identifier = '+'+str(friend.phone)
                    #print(phone)
                    country_code = None
                    phone = phoneparser(identifier,country_code)
                    contact_data = contact_upload(phone,user,request)
                    print("contact_data",contact_data)
                    return Response({'isSuccessful':True,'message':'Successfully find user','user':contact_data})
                else:
                    return Response({'isSuccessful':False,'message':'No user found'})
        except Exception as error:
            return Response({'isSuccessful':False,'message':'No user found'})

# Upload the Contact Data From User's Phone
class ContactUpload(APIView):
    def post(self,request):
        user_id = request.data['user_id']
        friend = request.data['contact']
        remove_space = friend.replace(" ","")
        split_friend = list(remove_space.split(","))
        user = User.objects.get(id=user_id)
        contact = []
        add = {'add':False}
        for phone in split_friend:
            try:
                if phone[0] == '+':
                    country_code = None
                    phone = phoneparser(phone,country_code)
                    if phone==None:
                        pass
                    else:
                        contact_data = contact_upload(phone,user,request)
                        contact.append(contact_data)
                elif phone.isdigit():
                    country_code = user.get_country_code()
                    phone = phoneparser(phone,country_code)
                    if phone==None:
                        pass
                    else:
                        contact_data = contact_upload(phone,user,request)
                        contact.append(contact_data)
                else:
                    pass
            except Exception:
                pass
        if contact==[]:
            return Response({"isSuccessful":False,'message':'No ChiChat User'})
        return Response({'isSuccessful':True,'message':'Successfully Load Contact','contact':contact})
# Sub Functions for Upload Contact (Parser the Phone)
def phoneparser(identifier,country_code):
    phone = phonenumbers.parse(identifier,country_code)
    phone = str(phone.country_code)+str(phone.national_number)
    if User.objects.filter(phone=phone).exists():
        friend = User.objects.get(phone=phone)
        return friend
    else:
        return None
# Sub Functions for Upload Contact (Find the Friend in Contact Upload)          
def contact_upload(phone,user,request):
    add = {'add':False}
    phone = ContactUploadSerializer({'contact':phone},context={"request":request})
    data = phone.data['contact']
    profile = UserProfile.objects.get(user_id=data['id'])
    if profile in user.contact.get_friends():
        add = {'add':True}
    else:
        pass
    data.update(add)
    del data['photo_url']
    return data

# User's Friend List
class FriendListView(APIView):
    def get(self,request,user_id):
        try:
            user = User.objects.get(id=user_id)
            requested_data = []
            for request_data in user.contact.get_friends():
                serializer = RegisterSerializer(request_data.user,context={"request": request})
                request_message = {}
                request_message.update(serializer.data)
                del request_message['photo_url']
                requested_data.append(request_message)
            if requested_data == []:
                return Response({'isSuccessful':False,'message':'No Friends Lists'})
            else:
                content = {'isSuccessful':True,'message':'Successfully Loaded Friend Lists'}
                content.update({'friend_lists':requested_data})
                return Response(content)
        except Exception:
            return Response({'isSuccessful':False}) """