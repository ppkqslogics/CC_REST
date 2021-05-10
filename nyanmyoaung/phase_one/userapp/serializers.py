from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from .models import *
import phonenumbers
import datetime
from profile_app.serializers import UserProfileSerializer
from PIL import Image
from django.core.files import File
from io import BytesIO
import os
from django.contrib.auth import login

def img_compress(photo):
    _, extension = os.path.splitext(photo.name)
    im = Image.open(photo)
    extension = str(extension.upper()).replace(".", "")
    im_io = BytesIO()
    if extension == "JPG":
        extension = "JPEG"
    else:
        pass
    im.save(im_io, extension, quality=50)
    new_image = File(im_io, name=photo.name)
    return new_image


class RegisterSerializer(serializers.ModelSerializer):
    '''
    Serializer for account creation \n
    INPUT : name, password, photo \n
    OUTPUT : serialized data \n
    FIELDS : id, name, phone, password, region, photo, chit_chat_id, photo_url \n
    Model : User
    '''
    password = serializers.CharField(
        max_length=255, min_length=2, write_only=True)
    photo = serializers.ImageField(
        allow_empty_file=True, use_url=True, default='default/default_profile_pic.jpg')
    photo_url = serializers.SerializerMethodField('get_photo_url')
    # token = serializers.JSONField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'password',
                  'region', 'photo', 'chit_chat_id', 'photo_url']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_photo_url(self, obj):
        request = self.context.get("request")
        print("======>", type(obj.photo))
        # return f'https://ccsecond.azurewebsites.net+{obj.photo.url}'
        return request.build_absolute_uri(obj.photo.url)

    def validate_phone(self, value):
        phone = phonenumbers.parse(value)
        phone = str(phone.country_code)+str(phone.national_number)
        return phone

    def validate_photo(self, photo):
        print("PHOTO", photo)
        if photo == "default/default_profile_pic.jpg":
            return photo
        else:
            new_image = img_compress(photo)
            print("======>new", type(new_image))
            return new_image


class PhoneLoginSerializer(serializers.ModelSerializer):
    """
    Authentication for login with phone
    INPUT : phone, password
    OUTPUT/RETURN : user profile
    FIELDs : phone, password, user
    """
    user = UserProfileSerializer(read_only=True)
    phone = serializers.CharField(max_length=17, min_length=2)
    password = serializers.CharField(
        max_length=255, min_length=2, write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'password', 'photo', 'user']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        phone = phonenumbers.parse(phone, None)
        phone = str(phone.country_code)+str(phone.national_number)
        password = attrs.get('password', '')
        user = auth.authenticate(phone=phone, password=password)

        if not user:
            raise AuthenticationFailed({'login': 'fail'})

        # login(request, user)

        return {'phone': user.phone, 'user': user.profile}


class IdLoginSerializer(serializers.ModelSerializer):
    """
    Authentication for login with chit chat id
    INPUT : chit_chat_id, password
    OUTPUT/RETURN : user profile
    FIELDs : chit_chat_id, password
    """
    chit_chat_id = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['chit_chat_id', 'password']

class ResetPasswordSerializer(serializers.Serializer):
    """
    NOT APPLIED 
    """
    phone = serializers.CharField(max_length=17, min_length=2)
    password = serializers.CharField(
        max_length=255, min_length=2, write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'password']


from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class RefreshTokenSerializer(TokenRefreshSerializer):
    # refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #     print("=====>", data)
    #     return data