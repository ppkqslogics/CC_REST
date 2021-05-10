from django.db import models
from userapp.models import User
from django.conf import settings
from datetime import datetime
from django.core.files import File
from PIL import Image
from io import BytesIO
import qrcode
# Create your models here.
def_cover_photo = 'default/default_cover.jpg'
gender_length = 30
qr_img_basewidth = 100
qr_fill_color = '#0000'
qr_back_color = 'white'

class Profile(models.Model):

    """
    INPUT(Required) : user \n
    INPUT(OPTIONal) : cover_photo, gender, birthday \n
    INPUT(AUTO ADDED): cover_photo, qr_img, created_at, updated_at \n
    LINKED MODEL : User \n
    RETURN : user
    """

    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    cover_photo = models.ImageField(
        upload_to='cover_photo', blank=True, default=def_cover_photo)
    qr_img = models.ImageField(upload_to='qr', blank=True)
    rank = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=gender_length, blank=True)
    birthday = models.DateField(blank=True, default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        img_io, fname, _ = make_qr_code(profile_pic=self.user.photo, user_ph=self.user.phone, user_cc_id=self.user.chit_chat_id)
        self.qr_img.save(fname, File(img_io), save=False)
        super().save(*args, **kwargs)

def make_qr_code(profile_pic, user_ph, user_cc_id):
    im = Image.open(profile_pic)
    wpercent = ((qr_img_basewidth/float(im.size[0])))
    hsize = int((float(im.size[1])*float(wpercent)))
    im = im.resize((qr_img_basewidth, hsize), Image.ANTIALIAS)
    qr_base_img = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr_base_img.add_data(f'chitchat://open.my.app/{user_ph}')
    qr_base_img.make()
    qr_base_img = qr_base_img.make_image(fill_color=qr_fill_color, back_color=qr_back_color).convert('RGB')
    pos = ((qr_base_img.size[0]-im.size[0])//2, (qr_base_img.size[1] - im.size[1])//2)
    qr_base_img.paste(im, pos)
    im_io = BytesIO()
    fname = f'{user_cc_id}_qr_code.png'
    qr_base_img.save(im_io, "PNG")
    return im_io, fname, im
