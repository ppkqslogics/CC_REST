from datetime import datetime

import phonenumbers
from profile_app.models import Profile
from profile_app.serializers import UserProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from services.firebase_manager import firebase_noti
from userapp.models import User
from rest_framework.permissions import IsAuthenticated
from contact_app.models import Contact, FriendsModel, Relationship, TagsModel
from contact_app.serializers import *
from setting_app.serializers import PrivacySerializer

# Create your views here.


class FriendRequestView(APIView):
    """
    INPUT : sender(id), receiver(id), message, (status auto added at serializer)
    SERIALIZER : RelationshipSerializer
    SUB_FUNC : firebase_noti
    OUTPUT/RES : message with serializer data
    """
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        fail_content = {
            "isSuccessful": False,
            'message': 'Friend Request Fail to Send'
        }
        try:
            sender = request.data['sender']
            receiver = request.data['receiver']
            if sender != receiver:
                obj_valid = True
                rs_obj = Relationship.objects.filter(
                    sender=sender, receiver=receiver)
                if rs_obj.exists():
                    obj_valid = False
                    return Response(fail_content)
                else:
                    rs_obj = Relationship.objects.filter(
                        sender=receiver, receiver=sender)
                    if rs_obj.exists():
                        obj_valid = False
                        return Response(fail_content)
                if obj_valid:
                    serializer = RelationshipSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        # data for fcm notification
                        sender_obj = User.objects.get(
                            id=serializer.data['sender'])
                        receiver_obj = User.objects.get(
                            id=serializer.data['receiver'])
                        # fcm token off...........>
                        # data = {
                        #     "title": "ChitChat",
                        #     "message": f"{sender_obj.name} sent you a friend request.",
                        #     "sender_img": request.build_absolute_uri(sender_obj.photo.url),
                        #     "phone": sender_obj.phone,
                        #     "category": "fri_req"
                        # }
                        # fcm_token = receiver_obj.fcm_token
                        # fcm noti subfunction
                        # response = firebase_noti(data, fcm_token)
                        return Response(
                            {
                                "isSuccessful": True,
                                'message': 'Friend request successfully sent',
                                'data': serializer.data
                            }, status=status.HTTP_200_OK)
                    else:
                        print(serializer.errors)
                        return Response(fail_content

                                        )
                else:
                    return Response(fail_content)
            else:
                return Response(fail_content)
        except Exception as error:
            print("ADD FRIEDND ERROR: ", error)
            return Response(fail_content, status=status.HTTP_400_BAD_REQUEST)


class ReceiverView(APIView):
    """
    View for list of requested friends
    INPUT : Get with user_id
    OUTPUT : Lists of friends request
    RETURN : Response message with lists of friends
    """
    permission_classes = [IsAuthenticated,]
    def get(self, request, user_id):
        try:
            req_user = Relationship.objects.filter(
                receiver=user_id, status="send")
            if req_user.count() != 0:
                serializer = FriendRequestListSerializer(
                    req_user, many=True, context={"request": request})
                return Response(
                    {
                        'isSuccessful': True,
                        'message': 'Successfully loaded friends request.',
                        'request_friend': serializer.data
                    }
                )
            else:
                content = {
                    'isSuccessful': True,
                    'message': 'No New Friends Request',
                    'request_friend': []
                }
                return Response(content, status=status.HTTP_200_OK)
        except Exception as error:
            print("RECEIVER VIEW ERROR: ", str(error))
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Failed to Load Friends Request'
                }, status=status.HTTP_400_BAD_REQUEST)


class ConfirmFriendView(APIView):
    """
    Confirm the friends from friends request
    INPUT : sender(id of requested friend), receiver(id of owner), nick_name
    OUTPUT : add friend to both user with confirmed status
    RETURN : response message
    """
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        try:
            sender = request.data['sender']
            receiver = request.data['receiver']
            nick_name = request.data['nick_name']
            print(request.data)
            rs_obj = Relationship.objects.filter(
                sender=sender, receiver=receiver)
            if rs_obj.exists():
                print("====>ok", rs_obj)
                send_user = User.objects.get(id=sender)
                receive_user = User.objects.get(id=receiver)
                print("====>ok1", send_user.contact,
                      receive_user.profile, nick_name)
                sender_contact = FriendsModelSerializer(data={
                    'owner': receive_user.contact,
                    'friend': send_user.profile,
                    'nick_name': nick_name
                })
                print("====>ok2", rs_obj)
                receiver_contact = FriendsModelSerializer(data={
                    'owner': send_user.contact,
                    'friend': receive_user.profile
                })
                print("====>ok3", rs_obj)
                if sender_contact.is_valid() and receiver_contact.is_valid():
                    print("====>validation")
                    sender_contact.save()
                    print("====>ok3", rs_obj)
                    receiver_contact.save()
                    print("====>ok3", rs_obj)
                    rs_obj.update(status='confirmed')
                    print("====>ok3", rs_obj)
                    friend = UserProfileSerializer(send_user.profile)
                    friend = friend.data
                    friend.update({'nick_name': nick_name})
                    print(friend)
                    return Response(
                        {
                            'isSuccessful': True,
                            'message': 'You are now friend',
                            'friend': friend
                        }, status=status.HTTP_200_OK)
                else:
                    print("====>notvalid")
                    print("====>ok", sender_contact.errors)
                    return Response(
                        {
                            'isSuccessful': False,
                            'message': 'Friend Request Failed to Confrim'
                        }
                    )
            else:
                return Response(
                    {
                        'isSuccessful': False,
                        'message': 'Friend Request Failed to Confrim'
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("CONFIRM FRIENDS ERRORS: ", str(error))
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Friend Request Failed to Confrim'
                }, status=status.HTTP_400_BAD_REQUEST)


class FindFriendView(APIView):
    '''
    Find the friend with phone or chitchat id \n
    INPUT : user_id, find_friend(phone (+95. or 09. or 9.) or chitchat id)\n
    OUTPUT : if found, friend profile with message or not, fail message
    '''
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        fail_content = {
            'isSuccessful': False,
            'message': 'No user found'
        }
        try:
            user = User.objects.get(id=request.data['user_id'])
            identifier = request.data['find_friend']
            # Phone no. starting with +95...
            if identifier[0] == '+':
                country_code = None
                phone = phoneparser(identifier, country_code)  # Ph parser
                contact_data = contact_upload(phone, user, request)
                if contact_data == "":
                    return Response(fail_content)
                else:
                    contact_data = fri_req_condition(
                        contact_data, request, phone)
                    return Response(
                        {
                            'isSuccessful': True,
                            'message': 'Successfully find user',
                            'user': contact_data
                        }, status=status.HTTP_200_OK)
            # Ph no. starting with 09 or 9
            elif identifier.isdigit():
                country_code = user.get_country_code()
                phone = phoneparser(identifier, country_code)
                contact_data = contact_upload(phone, user, request)
                if contact_data == "":
                    return Response(fail_content)
                else:
                    contact_data = fri_req_condition(
                        contact_data, request, phone)
                    return Response(
                        {
                            'isSuccessful': True,
                            'message': 'Successfully find user',
                            'user': contact_data
                        }, status=status.HTTP_200_OK)
            # for ccid
            else:
                user_obj = User.objects.filter(chit_chat_id=identifier)
                if user_obj.exists():
                    user_obj = user_obj.first()
                    identifier = '+'+str(user_obj.phone)
                    country_code = None
                    phone = phoneparser(identifier, country_code)
                    contact_data = contact_upload(phone, user, request)
                    if contact_data == "":
                        return Response(fail_content)
                    else:
                        contact_data = fri_req_condition(
                            contact_data, request, phone)
                        return Response(
                            {
                                'isSuccessful': True,
                                'message': 'Successfully find user',
                                'user': contact_data
                            }, status=status.HTTP_200_OK)
                else:
                    return Response(fail_content)
        except Exception as error:
            print("FIND FRIEND VIEW ERROR: ", str(error))
            return Response(fail_content, status=status.HTTP_400_BAD_REQUEST)

# sub function for fri req sent or not


def fri_req_condition(contact_data, request, phone):
    print("====>", contact_data)
    privacy_obj = PrivacySerializer(phone.privacy)
    if not contact_data['add']:
        fri_req_sender = Relationship.objects.filter(
            sender=contact_data['id'], receiver=request.data['user_id'])
        fri_req_receiver = Relationship.objects.filter(
            sender=contact_data['id'], receiver=request.data['user_id'])
        if fri_req_sender.exists() or fri_req_receiver.exists():
            fri_req_sent = True
        else:
            fri_req_sent = False
    else:
        fri_req_sent = False
    contact_data.update({"privacy": privacy_obj.data})
    contact_data.update({'fri_req_sent': fri_req_sent})
    return contact_data


class ContactUpload(APIView):
    """
    Mobile Contact upload view \n
    INPUT : user_id, contact (ph, ph, ph,)
    OUTPUT : chit chat user list with friend or not
    """
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        fail_content = {
            "isSuccessful": False,
            'message': 'No ChiChat User'
        }
        try:
            user_id = request.data['user_id']
            friend = request.data['contact']
            remove_space = friend.replace(" ", "")
            split_friend = list(remove_space.split(","))
            split_friend = [space for space in split_friend if space not in '']
            user = User.objects.get(id=user_id)
            contact = []
            for phone in split_friend:
                if phone[0] == '+':
                    country_code = None
                    phone = phoneparser(phone, country_code)
                    if phone is None:
                        pass
                    else:
                        contact_data = contact_upload(phone, user, request)
                        if contact_data == "":
                            pass
                        else:
                            fri_req_condition(contact_data, request, phone)
                            contact.append(contact_data)
                elif phone.isdigit():
                    country_code = user.get_country_code()
                    phone = phoneparser(phone, country_code)
                    if phone is None:
                        pass
                    else:
                        contact_data = contact_upload(phone, user, request)
                        if contact_data == "":
                            pass
                        else:
                            fri_req_condition(contact_data, request, phone)
                            contact.append(contact_data)
                else:
                    pass
            if contact == []:
                return Response(fail_content)
            return Response(
                {
                    'isSuccessful': True,
                    'message': 'Successfully Load Contact',
                    'contact': contact
                }, status=status.HTTP_200_OK)
        except Exception as error:
            print("CONTACT UPLOAD ERROR: ", str(error))
            return Response(fail_content, status=status.HTTP_400_BAD_REQUEST)

# Pharser for phone using phonenumbers library


def phoneparser(identifier, country_code):
    phone = phonenumbers.parse(identifier, country_code)
    phone = str(phone.country_code)+str(phone.national_number)
    if User.objects.filter(phone=phone).exists():
        friend = User.objects.get(phone=phone)
        return friend
    else:
        return None

# sub func: for the person is fri with user or not
# if fri : True and not for False


def contact_upload(phone, user, request):
    add = {'add': False}
    if (user.profile in phone.contact.block_list.all()) or (phone.profile in user.contact.block_list.all()):
        return ""
    else:
        phone = FriendProfileSerializer(phone.profile, context={
            "request": request,
            "owner": user.contact
        })
        data = phone.data
        profile = Profile.objects.get(user_id=data['id'])
        if profile in user.contact.get_friends():
            add = {'add': True}
        else:
            pass
        data.update(add)
        return data


class FriendListView(APIView):
    """
    Get the friends list \n
    INPUT : user_id with get method \n
    OUTPUT/RETURN : Lists of friends with message
    """
    #permission_classes = [IsAuthenticated,]
    def get(self, request, user_id):
        try:
            contact_obj = Contact.objects.get(user=user_id)
            if contact_obj.friends.all() == 0:
                return Response(
                    {
                        'isSuccessful': True,
                        'message': 'No Friends Lists',
                        'friend_lists': []
                    }, status=status.HTTP_200_OK)
            else:
                print("====>", contact_obj.friendsmodel_set.all())
                serializer = FriendsListSerializer(contact_obj.friendsmodel_set.all(), context={
                    "request": request,
                }, many=True)
                return Response(
                    {
                        'isSuccessful': True,
                        'message': 'Successfully Loaded Friend Lists',
                        'friend_lists': serializer.data
                    }, status=status.HTTP_200_OK)
        except Exception as error:
            print("FRIEND LISTS ERROR: ", error)
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'No Friends Lists'
                }, status=status.HTTP_400_BAD_REQUEST)


class EditContact(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        try:
            user_obj = Contact.objects.get(user=request.data['user_id'])
            friend_obj = Profile.objects.get(user=request.data['friend_id'])
            friend_model = user_obj.friendsmodel_set.get(friend=friend_obj)
            friend_model.nick_name = request.data['nick_name']
            friend_model.save()
            return Response(
                {
                    'isSuccessful': True,
                    'message': 'Successfully changed nickname.',
                }
            )
        except Exception as error:
            print("CONTACT EDIT ERROR: ", error)
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Fail to change nickname.'
                }, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        pass


class DeleteContact(APIView):
    """
    For contact delete (unfriend)
    INPUT : user_id, friend_id
    MODEL_USE : Relationship, User.Contact
    OUTPUT\RES : message 
    """
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        try:
            user_obj = User.objects.get(id=request.data['user_id'])
            friend_obj = User.objects.get(id=request.data['friend_id'])
            rs_obj = Relationship.objects.filter(
                sender=user_obj.profile, receiver=friend_obj.profile)
            if rs_obj.exists():
                remove_friend(user_obj, friend_obj)
                print("rs_obj_1")
                rs_obj = rs_obj.first()
                rs_obj.delete()
                print(rs_obj)
            else:
                rs_obj = Relationship.objects.filter(
                    sender=friend_obj.profile, receiver=user_obj.profile)
                if rs_obj.exists():
                    remove_friend(user_obj, friend_obj)
                    print("rs_obj_2")
                    rs_obj = rs_obj.first()
                    rs_obj.delete()
            return Response(
                {
                    'isSuccessful': True,
                    'message': 'Successfully delete contact'
                }
            )
        except Exception as error:
            print("DELETE CONTACT ERROR: ", error)
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Fail to delete contact'
                }, status=status.HTTP_400_BAD_REQUEST)


def remove_friend(user_obj, friend_obj):
    user_obj.contact.friends.remove(friend_obj.profile)
    friend_obj.contact.friends.remove(user_obj.profile)
    for tag in user_obj.contact.tagsmodel_set.all():
        if friend_obj.profile in tag.tagged_member.all():
            tag.tagged_member.remove(friend_obj.profile)
        else:
            pass
    for tag in friend_obj.contact.tagsmodel_set.all():
        if user_obj.profile in tag.tagged_member.all():
            tag.tagged_member.remove(user_obj.profile)
        else:
            pass


class EditContactTag(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, user_id, friend_id):
        fail_content = {
            'isSuccessful': False,
            'message': 'Fail to load edit contact'
        }
        try:
            contact_obj = Contact.objects.get(user_id=user_id)
            fri_profile = Profile.objects.get(user_id=friend_id)
            print("====>okdata")
            fri_model = contact_obj.friendsmodel_set.filter(friend=fri_profile)
            print("====>okfrimodel")
            if fri_model.exists():
                print("====>frimodelexit")
                fri_model = fri_model.first()
                fri_nick_name = fri_model.nick_name
                fri_tags = []
                print("====>ok")
                for tag in contact_obj.tagsmodel_set.all():
                    print("====>ok", tag)
                    if fri_profile in tag.tagged_member.all():
                        print("====>seri")
                        tag_obj = EditTagSerializer(tag)
                        fri_tags.append(tag_obj.data)
                    else:
                        pass
                return Response(
                    {
                        'isSuccessful': True,
                        'name': fri_profile.user.name,
                        'phone': f'+{fri_profile.user.phone}',
                        'nick_name': fri_nick_name,
                        'tags': fri_tags
                    }
                )
            else:
                return Response(fail_content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print("EDIT CONTACT GET ERROR: ", error)
            return Response(fail_content, status=status.HTTP_400_BAD_REQUEST)


class EditContactAllTags(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, user_id, friend_id):
        try:
            contact_obj = Contact.objects.get(user_id=user_id)
            fri_obj = Profile.objects.get(user_id=friend_id)
            tag_obj = contact_obj.tagsmodel_set.all()
            serializer = EditAllTagSerializer(
                tag_obj, many=True, context={"fri_obj": fri_obj})
            return Response(
                {
                    'isSuccessful': True,
                    'tags': serializer.data,
                }
            )
        except Exception as error:
            print("EDIT CONTACT ALL TAGS ERROR: ", error)
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Fail to get data'
                }
            )


class EditContactAddTag(APIView):

    """
    INPUT : user_id, friend_id, tag_name, tag_id \n
    RESPONSE : messages \n
    MODEL : Contact, Profile \n
    SERIALIZER : TagsModelSerializer \n 
    URL : /edit_contact_add_tag/ \n
    METHOD : POST
    SUB FUNC : add_remove_tag(contact_obj, fri_obj, list_obj)
    """
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        success_content = {
            'isSuccessful': True,
            'message': 'Successfully edit tag.'
        }
        try:
            contact_obj = Contact.objects.get(user_id=request.data['user_id'])
            fri_obj = Profile.objects.get(user_id=request.data['friend_id'])
            tag_name = request.data['tag_name']
            tag_id = request.data['tag_id']
            # remove unwanted data
            remove_space = tag_id.replace(" ", "")
            list_obj = list(remove_space.split(","))
            list_obj = [
                space for space in list_obj if space not in '']
            # if == "", create new tag
            if tag_name == "":
                add_remove_tag(contact_obj, fri_obj, list_obj)
                return Response(success_content)
            # edit tag
            else:
                is_tag = False
                # condition for tag is in user tag list
                for tag in contact_obj.tagsmodel_set.all():
                    if tag_name in tag.tag_name:
                        add_remove_tag(contact_obj, fri_obj, list_obj)
                        if fri_obj in tag.tagged_member.all():
                            pass
                        else:
                            tag.tagged_member.add(fri_obj)
                        is_tag = True
                    else:
                        pass
                # if not creat tag
                if not is_tag:
                    add_remove_tag(contact_obj, fri_obj, list_obj)
                    fri_obj_list = []
                    fri_obj_list.append(fri_obj.user_id)
                    serializer = TagsModelSerializer(data={
                        'owner': contact_obj,
                        'tag_name': tag_name,
                        'tagged_member': fri_obj_list
                    })
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        pass
                else:
                    pass
                return Response(success_content)

        except Exception as error:
            print("EDIT CONTACT ADD TAG ERROR: ", error)
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Fail to edit tag.'
                }, status=status.HTTP_400_BAD_REQUEST
            )


def add_remove_tag(contact_obj, fri_obj, list_obj):
    origin_tag_list = []
    for tag in contact_obj.tagsmodel_set.all():
        if fri_obj in tag.tagged_member.all():
            origin_tag_list.append(tag.tag_id)
    add_tag = set(list_obj)-set(origin_tag_list)
    remove_tag = set(origin_tag_list)-set(list_obj)
    for add in list(add_tag):
        tag = contact_obj.tagsmodel_set.filter(tag_id=add)
        if tag.exists():
            tag = tag.first()
            tag.tagged_member.add(fri_obj)
        else:
            pass
    for remove in list(remove_tag):
        tag = contact_obj.tagsmodel_set.filter(tag_id=remove)
        if tag.exists():
            tag = tag.first()
            tag.tagged_member.remove(fri_obj)
            if tag.tagged_member.all().count() == 0:
                tag.delete()
            else:
                pass
        else:
            pass


class TagsView(APIView):

    """
    For add tag and edit tag
    INPUT : user_id, tag_name, tag_id, tagged_member
    RESPONSE : messages
    ADD : tag_id = 'null'
    EDIT : tag_id = tag_id
    MODEL : User, Contact, TagsModel
    SERIALIZER : TagsModelSerializer
    """
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        try:
            user = User.objects.get(id=request.data['user_id'])
            tag_name = request.data['tag_name']
            tag_id = request.data['tag_id']
            tagged_member = request.data['tagged_member']
            # Remove unwanted data (' ', ',')
            remove_space = tagged_member.replace(" ", "")
            split_tag_member = list(remove_space.split(","))
            split_tag_member = [
                space for space in split_tag_member if space not in '']
            # condition for tagged member is in user friend list
            no_friend = True
            for friend_id in split_tag_member:
                friend_obj = Profile.objects.get(user_id=friend_id)
                if friend_obj in user.contact.friends.all():
                    pass
                else:
                    no_friend = False
                    break
            # no error if no_friend is True
            if no_friend:
                # condition for create or edit, 'null' is to create
                if tag_id == 'null':
                    serializer = TagsModelSerializer(data={
                        'owner': user.contact,
                        'tag_name': tag_name,
                        'tagged_member': split_tag_member
                    })
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                            {
                                'isSuccessful': True,
                                'message': 'Successfully tagged members'
                            }, status=status.HTTP_201_CREATED)
                    else:
                        return Response(
                            {
                                'isSuccessful': False,
                                'message': 'Tag name already exist'
                            }, status=status.HTTP_403_FORBIDDEN)
                # for tag edit
                else:
                    tag_obj = TagsModel.objects.filter(
                        tag_id=tag_id, owner=user.contact)
                    if tag_obj.exists():
                        # there is no member in tag, it will delete automatically
                        if split_tag_member == []:
                            tag_obj = tag_obj.first()
                            tag_name = tag_obj.tag_name
                            tag_obj.delete()
                            return Response(
                                {
                                    'isSuccessful': True,
                                    'message': f'There is no member in tag, {tag_name} tag is deleted'
                                }
                            )
                        # if there is member, it will add or remove member
                        else:
                            tag_obj.update(tag_name=tag_name,
                                           updated_at=datetime.now())
                            tag_obj = tag_obj.first()
                            tag_obj.tagged_member.clear()
                            for tag in split_tag_member:
                                tag_obj.tagged_member.add(tag)
                            return Response(
                                {
                                    'isSuccessful': True,
                                    'message': 'Successfully tagged members'
                                }, status=status.HTTP_200_OK)
                    else:
                        return Response(
                            {
                                'isSuccessful': False,
                                'message': 'There is no such tag'
                            }
                        )
            else:
                tag_obj = TagsModel.objects.filter(
                    tag_id=tag_id, owner=user.contact)
                if tag_obj.exists():
                    tag_obj = tag_obj.first()
                    tag_obj.delete()
                    return Response(
                        {
                            'isSuccessful': False,
                            'message': f'There is no member in tag, {tag_name} tag is deleted'
                        }, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {
                            'isSuccessful': False,
                            'message': 'There is no such tag'
                        }
                    )
        except Exception as error:
            print("TagsViewErrors: ", str(error))
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Fail to create/edit tag'
                }, status=status.HTTP_400_BAD_REQUEST)


class TagDeleteView(APIView):

    """
    INPUT : user_id, tag_id \n
    RESPONSE : messages \n
    MODEL : TagsModel \n
    SERIALIZER : -\n 
    URL : /delete_tag/ \n
    METHOD : POST
    """
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        try:
            user_id = request.data['user_id']
            tag_id = request.data['tag_id']
            tag = TagsModel.objects.filter(tag_id=tag_id, owner_id=user_id)
            if tag.exists():
                tag = tag.first()
                tag_name = tag.tag_name
                tag.delete()
                return Response(
                    {
                        'isSuccessful': True,
                        'message': f'{tag_name} tag is deleted'
                    }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        'isSuccessful': False,
                        'message': 'Tag does not exit.'
                    }
                )
        except Exception as error:
            print("TAG DELETE VIEW ERROR: ", str(error))
            return Response(
                {
                    'isSuccessful': False,
                    'message': f'fail to delete tag'
                }, status=status.HTTP_400_BAD_REQUEST)


class TagsListView(APIView):

    """
    INPUT : user_id\n
    RESPONSE : tag lists\n
    MODEL : Contact\n
    SERIALIZER : TagsListSerializer \n 
    URL : /tag_list/<user_id>/ \n
    METHOD : GET
    """
    permission_classes = [IsAuthenticated,]
    def get(self, request, user_id):
        try:
            contact_obj = Contact.objects.get(user_id=user_id)
            tags = contact_obj.tagsmodel_set.all()
            serializer = TagsListSerializer(
                tags, many=True, context={"request": request})
            return Response(
                {
                    'isSuccessful': True,
                    'message': 'Successfully loaded tag lists',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
        except Exception as error:
            print("TagsListViewErrors: ", str(error))
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Fail to load tag lists'
                }, status=status.HTTP_400_BAD_REQUEST)


class FriendBlockView(APIView):

    """
    Friend block
    INPUT : user_id, friend_id \n
    RESPONSE : messages \n
    MODEL : User, Profile, Contact, Relationship \n
    SERIALIZER : - \n 
    URL : /block_friend/ \n
    METHOD : POST
    """
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        try:
            user_id = request.data['user_id']
            friend_id = request.data['friend_id']
            user_obj = User.objects.get(id=user_id)
            friend_obj = User.objects.get(id=friend_id)
            rs_obj_one = Relationship.objects.filter(
                sender=user_obj.profile, receiver=friend_obj.profile)
            rs_obj_two = Relationship.objects.filter(
                sender=friend_obj.profile, receiver=user_obj.profile)
            rs_obj = rs_obj_one or rs_obj_two
            user_obj.contact.friends.remove(friend_obj.profile)
            friend_obj.contact.friends.remove(user_obj.profile)
            remove_friend_from_tag(first_obj=user_obj, second_obj=friend_obj)
            remove_friend_from_tag(first_obj=friend_obj, second_obj=user_obj)
            if rs_obj.exists():
                rs_obj.update(status='block')
            else:
                relation = Relationship(
                    sender=user_obj.profile, receiver=friend_obj.profile, status='block')
                relation.save()
            user_obj.contact.block_list.add(friend_obj.profile)
            return Response(
                {
                    'isSuccessful': True,
                    'message': 'Successfully block contact.'
                }
            )
        except Exception as error:
            print("DELETE CONTACT ERROR: ", error)
            return Response(
                {
                    'isSuccessful': False,
                    'message': 'Fail to block contact'
                }, status=status.HTTP_400_BAD_REQUEST)


def remove_friend_from_tag(first_obj, second_obj):

    """
    Remove blocked friend from user tags
    Use : FriendBlockView
    """

    for tag in first_obj.contact.tagsmodel_set.all():
        if second_obj.profile in tag.tagged_member.all():
            tag.tagged_member.remove(second_obj.profile)
        else:
            pass
