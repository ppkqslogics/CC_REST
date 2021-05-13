from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required 

urlpatterns = [
    path('profile/<user_id>/', (views.UserProfileView.as_view()), name="profile"),
#     path('profile/<user_id>/', login_required(views.UserProfileView.as_view(), login_url = 'another'), name="profile"),
    path('friend_profile/<user_id>/',
         login_required(views.FriendProfileView.as_view(), login_url = 'another'), name="friend_profile"),
    path('stranger_profile/<user_id>/',
         login_required(views.StrangerProfileView.as_view(), login_url = 'another'), name="stranger_profile"),
    path('change_name/', login_required(views.update_name, login_url = 'another'), name="change_name"),
    path('change_photo/', login_required(views.update_photo, login_url = 'another'), name="change_photo"),
    path('change_cover_photo/', login_required(views.update_cover_photo, login_url = 'another'),
         name="change_cover_photo"),
    path('change_region/', login_required(views.update_region, login_url = 'another'), name="change_region"),
    path('change_birthday/', login_required(views.update_birthday, login_url = 'another'), name="change_birthday"),
    path('change_gender/', login_required(views.update_gender, login_url = 'another'), name="change_gender"),
    path('api/', login_required(views.testapi, login_url = 'another'), name="api"),
]
