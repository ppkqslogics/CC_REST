from rest_framework import serializers
from .models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    '''
    UserProfileSerializer \n
    INPUT : user_data, cover_photo, rank, gender, birthday \n
    OUTPUT : serialized user profile
    '''
    id = serializers.IntegerField(source='user.id')
    name = serializers.CharField(max_length=30, source='user.name')
    phone = serializers.CharField(max_length=30, source='user.phone')
    # photo = serializers.ImageField(source='user.photo')
    photo = serializers.SerializerMethodField('get_photo')
    chit_chat_id = serializers.CharField(
        max_length=30, source='user.chit_chat_id')
    cover_photo = serializers.SerializerMethodField('get_cover_photo')
    # cover_photo = serializers.ImageField(
    #     allow_empty_file=True, use_url=True, default='default/default_cover.jpg')
    region = serializers.CharField(max_length=30, source='user.region')
    birthday = serializers.DateField(format="%d/%m/%Y")
    qr_img = serializers.SerializerMethodField('get_qr')
    # token = serializers.JSONField(read_only=True, source='user.tokens')

    class Meta:
        model = Profile
        exclude = ['user', 'created_at', 'updated_at']

    def get_photo(self, obj):
        photo_url = obj.user.photo.url
        return f'https://ccsecond.azurewebsites.net{photo_url}'

    def get_cover_photo(self, obj):
        cover_photo_url = obj.cover_photo.url
        return f'https://ccsecond.azurewebsites.net{cover_photo_url}'

    def get_qr(self, obj):
        qr_url = obj.qr_img.url
        return f'https://ccsecond.azurewebsites.net{qr_url}'

    # def validate_cover_photo(self, value):
    #     print("==============here====")
    #     request = self.context.get("request")
    #     # return f'{request}+{value.url}'
    #     return request.build_absolute_uri(value.url)

    # def validate_qr_img(self, value):
    #     request = self.context.get("request")
    #     # return f'{request}+{value.url}'
    #     return request.build_absolute_uri(value.url)

