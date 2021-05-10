from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .id_generator import random_generator
import phonenumbers
import datetime
from django.utils import timezone

max_name = 30
max_region = 100
max_password = 100
max_phone = 20
max_chit_chat_id = 12
min_chit_chat_id = 8
gender = 6
otp_length = 6
photo_local = "photo/%Y/%m/%d"
photo_default_local = 'default/default_profile_pic.jpg'


def unique_generator():
    '''
    Filter the random id to be uniqued
    '''
    unique_id = random_generator()
    try:
        while User.objects.filter(chit_chat_id=unique_id).exists():
            unique_id = random_generator()
        return unique_id
    except Exception:
        return unique_id


class UserManager(BaseUserManager):
    '''
    User Manager between Normal User and Super User
    '''

    def create_user(self, phone, password=None, **extrafield):
        user = self.model(phone=phone, **extrafield)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None):
        if password is None:
            raise TypeError("Enter Password")
        user = self.create_user(phone, password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    """
    CREATED USING DJANGO BASE USER MODEL
    INPUT(Required) : name, phone, password, fcm_token \n
    INPUT(OPTIONal) : region, photo \n
    INPUT(AUTO ADDED): photo, chit_chat_id, is_verified, is_staff, is_superuser, is_active, updated_at, created_at, ccid_updated_at \n
    LINKED MODEL : - \n
    RETURN : name, tokens, country code
    """
    name = models.CharField(max_length=max_name, blank=True)
    region = models.CharField(max_length=max_region, blank=True)
    phone = models.CharField(max_length=max_phone, unique=True)
    photo = models.ImageField(upload_to=photo_local,
                              blank=True, default=photo_default_local)
    chit_chat_id = models.CharField(
        max_length=max_chit_chat_id, default=unique_generator, unique=True)
    fcm_token = models.CharField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ccid_updated_at = models.DateTimeField(blank=True, null=True)
    # ccid_updated_at = models.DurationField(default=datetime.timedelta(days=0, hours=0, minutes=0, seconds=0),blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELS = []

    objects = UserManager()

    def __str__(self):
        return self.name

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        # return str(refresh.access_token)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

    def get_country_code(self):
        phone = str('+')+str(self.phone)
        phone = phonenumbers.parse(phone)
        country_code = phonenumbers.region_code_for_number(phone)
        return str(country_code)


class PhoneOTP(models.Model):
    """
    **NOT APPLIED NOW"
    INPUT : phone, otp(generated), counts(default)
    OUTPUT : phone, otp, count, created_at
    RETURN : return phone number
    """
    phone = models.CharField(max_length=max_phone, unique=True)
    otp = models.CharField(max_length=otp_length)
    counts = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.phone

from django.conf import settings
from django.db import models
from django.contrib.sessions.models import Session

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)

from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver

@receiver(user_logged_in)
def remove_other_sessions(sender, user, request, **kwargs):
    # remove other sessions
    try:
        #sec = Session.objects.filter(usersession__user=user).delete()
        # print(sec)
        #a = Session.objects.filter(usersession__user=user).exclude(session_key=sec.first()).delete()
        #print("=====>",a)

        # create a link from the user to the current session (for later removal)
        UserSession.objects.get_or_create(
            user=user,
            session=Session.objects.get(pk=request.session.session_key)
        )
        sec = Session.objects.filter(usersession__user=user).order_by('-expire_date')
        print("====>count", sec.count())
        if sec.count()<2:
            print("here")
            pass
        else:
            a = Session.objects.filter(usersession__user=user).exclude(session_key=sec.first()).delete()
            print("=====>",a)
        # save current session
        request.session.save()
    except Exception as error:
        print("ERRRRRRRR===>", error)
