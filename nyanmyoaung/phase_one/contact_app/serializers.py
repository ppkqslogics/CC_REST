from rest_framework import serializers
from datetime import datetime, timezone
from .models import Contact, FriendsModel, Relationship, TagsModel
from userapp.serializers import RegisterSerializer, UserProfileSerializer
from profile_app.models import Profile
from setting_app.serializers import PrivacySerializer


class RelationshipSerializer(serializers.ModelSerializer):
    """
    Serializer for the relationship of two user \n
    INPUT : sender, receiver, message, status (auto added) \n
    OUTPUT : serialized data \n
    MODEL : Relationship
    """
    request_message = serializers.CharField(max_length=30, allow_blank=True)
    status = serializers.CharField(
        max_length=30, default='send', allow_blank=True)

    class Meta:
        model = Relationship
        fields = ['sender', 'receiver', 'request_message', 'status']


class ContactUploadSerializer(serializers.Serializer):
    """
    Serializer for contactupload \n
    INPUT : contact data \n
    OUTPUT : serialized contact data
    """
    contact = RegisterSerializer(read_only=True)
    """ class Meta:
        model = User
        fields = ['contact']  """


class FriendListSerializer(serializers.Serializer):
    friend_list = RegisterSerializer(read_only=True, many=True)


class FriendRequestListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='sender_id')
    name = serializers.CharField(max_length=30, source='sender.user.name')
    phone = serializers.CharField(max_length=30, source='sender.user.phone')
    region = serializers.CharField(max_length=30, source='sender.user.region')
    photo = serializers.ImageField(source='sender.user.photo')
    cover_photo = serializers.ImageField(source='sender.cover_photo')
    chit_chat_id = serializers.CharField(
        max_length=30, source='sender.user.chit_chat_id')
    sent_at = serializers.SerializerMethodField('get_sent_at')

    class Meta:
        model = Relationship
        exclude = ['status', 'created_at', 'updated_at', 'sender', 'receiver']

    def get_sent_at(self, obj):
        time_now = datetime.now(timezone.utc)
        time_diff = time_now - obj.created_at
        print("++++++++>",time_now)
        print("++++++++>",obj.created_at)
        print("++++++++>",time_diff, time_diff.seconds)
        seconds = time_diff.seconds
        days = time_diff.days
        minutes = seconds // 60
        if minutes>60:
            hours =  minutes // 60
            if hours > 24:
                days = days
                if days > 7:
                    weeks = days // 7
                    if weeks > 48:
                        years = weeks // 48
                        return f'{years} y'
                    else:
                        return f'{weeks} w'
                else:
                    return f'{days} d'
            else:
                return f'{hours} h'
        else:
            return f'{minutes} m'
        print("=====>", time_diff.days)


class FriendsModelSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(source='friend.user.id', read_only=True)
    # name = serializers.CharField(max_length=30, source='friend.user.name',  read_only=True)
    # phone = serializers.CharField(max_length=30, source='friend.user.phone',  read_only=True)
    # photo = serializers.ImageField(source='friend.user.photo', read_only=True)
    # chit_chat_id = serializers.CharField(
    #     max_length=30, source='friend.user.chit_chat_id', read_only=True)
    # cover_photo = serializers.ImageField(source='friend.cover_photo', read_only=True)
    # region = serializers.CharField(max_length=30, source='friend.user.region', read_only=True)
    # birthday = serializers.DateField(source='friend.birthday',format="%d/%m/%Y", read_only=True)
    class Meta:
        model = FriendsModel
        # exclude = ['owner','friend','created_at']
        fields = '__all__'

class FriendsListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='friend.user.id', read_only=True)
    name = serializers.CharField(max_length=30, source='friend.user.name',  read_only=True)
    nick_name = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=30, source='friend.user.phone',  read_only=True)
    photo = serializers.ImageField(source='friend.user.photo', read_only=True)
    chit_chat_id = serializers.CharField(
        max_length=30, source='friend.user.chit_chat_id', read_only=True)
    cover_photo = serializers.ImageField(source='friend.cover_photo', read_only=True)
    region = serializers.CharField(max_length=30, source='friend.user.region', read_only=True)
    birthday = serializers.DateField(source='friend.birthday',format="%d/%m/%Y", read_only=True)
    privacy = serializers.SerializerMethodField('get_privacy')
    class Meta:
        model = FriendsModel
        exclude = ['owner','friend','created_at','updated_at']
    
    def get_privacy(self, obj):
        privacy = PrivacySerializer(obj.friend.user.privacy)
        return privacy.data

class TagsModelSerializer(serializers.ModelSerializer):
    """
    Serializer for tag \n
    INPUT : tag_id(null), tag_name, tagged_member, owner \n
    OUTPUT : serialized tag data \n
    MODEL : TagsModel
    """
    class Meta:
        model = TagsModel
        fields = ['tag_id', 'tag_name', 'tagged_member', 'owner']

class FriendProfileSerializer(serializers.ModelSerializer):
    '''
    UserProfileSerializer \n
    INPUT : user_data, cover_photo, rank, gender, birthday \n
    OUTPUT : serialized user profile
    '''
    id = serializers.IntegerField(source='user.id')
    name = serializers.CharField(max_length=30, source='user.name')
    nick_name = serializers.SerializerMethodField('get_nick_name')
    phone = serializers.CharField(max_length=30, source='user.phone')
    photo = serializers.ImageField(source='user.photo')
    chit_chat_id = serializers.CharField(
        max_length=30, source='user.chit_chat_id')
    cover_photo = serializers.ImageField(
        allow_empty_file=True, use_url=True, default='default/default_cover.jpg')
    region = serializers.CharField(max_length=30, source='user.region')
    birthday = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Profile
        exclude = ['user', 'created_at', 'updated_at', 'qr_img']

    def get_nick_name(self, obj):
        owner = self.context.get("owner")
        try:
            nick_name = owner.friendsmodel_set.get(friend = obj.user.id)
            nick_name = nick_name.nick_name
            return nick_name
        except Exception:
            return ""

class TagsListSerializer(serializers.ModelSerializer):
    tag_id = serializers.CharField(max_length=20)
    tag_name = serializers.CharField(max_length=100)
    count = serializers.SerializerMethodField('get_count')
    user = serializers.SerializerMethodField('get_user_list')

    class Meta:
        model = TagsModel
        # fields = '__all__'#['like_count']
        exclude = ['id', 'created_at', 'updated_at', 'owner', 'tagged_member']

    # get tag count
    def get_count(self, obj):
        return obj.tagged_member.all().count()

    # get timeline image lists
    def get_user_list(self, obj):
        # serializer = FriendsListSerializer(contact_obj.friendsmodel_set.all(), context={"request": request}, many=True)
        tag_mem = obj.tagged_member.all()
        owner = obj.owner
        if tag_mem.count() != 0:
            request = self.context.get("request")
            tag_mem_list = FriendProfileSerializer(tag_mem, context={"request": request, "owner":obj.owner}, many=True)
            tag_mem_list = tag_mem_list.data
        else:
            tag_mem_list = []
        return tag_mem_list

class EditTagSerializer(serializers.ModelSerializer):
    added = serializers.BooleanField(default=True, read_only=True)
    class Meta:
        model = TagsModel
        fields = ['tag_id', 'tag_name', 'added']

class EditAllTagSerializer(serializers.ModelSerializer):
    added = serializers.SerializerMethodField('get_status')
    class Meta:
        model = TagsModel
        fields = ['tag_id', 'tag_name', 'added']

    def get_status(self, obj):
        fri_obj = self.context.get("fri_obj")
        if fri_obj in obj.tagged_member.all():
            return True
        else:
            return False
            
