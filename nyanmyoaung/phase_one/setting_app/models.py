from django.db import models
from userapp.models import User

""" class AccountSecurity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_changed_date = models.DateField(blank=True, null=True)
    id_changeable_date = models.DateTimeField(blank=True,null=True)
    id_changeable = models.BooleanField(default=True)
    account_cancellation = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) """

class Privacy(models.Model):

    """
    INPUT(Required) : user, req_msg
    INPUT(OPTIONal) : -
    INPUT(AUTO ADDED): updated_at
    LINKED MODEL : User
    RETURN : user
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    req_msg = models.BooleanField(default=False)
    # recommend_me = models.BooleanField(default=True)
    # visible_to = models.CharField(max_length=20, default='Everyone')
    # visible_time = models.CharField(max_length=20, default='Everytime')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

class SettingNotification(models.Model):

    """
    INPUT(Required) : user, req_msg
    INPUT(OPTIONal) : -
    INPUT(AUTO ADDED): updated_at
    LINKED MODEL : User
    RETURN : user
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    msg_noti = models.BooleanField(default=True)
    dating_noti = models.BooleanField(default=True)
    secret_msg_noti = models.BooleanField(default=True)
    call_noti = models.BooleanField(default=True)
    private_noti = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

class General(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=30, default="English")
    auto_download_hd = models.BooleanField(default=True)
    auto_save_photo = models.BooleanField(default=True)
    auto_save_video = models.BooleanField(default=True)
    auto_play_moblie = models.BooleanField(default=True)
    auto_play_wifi = models.BooleanField(default=True)
    moments = models.BooleanField(default=True)
    dating = models.BooleanField(default=True)
    secret_letter = models.BooleanField(default=True)
    cc_fri = models.BooleanField(default=True)
    games = models.BooleanField(default=True)
    sticker_gallery = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
