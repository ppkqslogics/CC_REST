from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('privacy/<user_id>/', login_required(views.PrivacyView.as_view()), name="privacy"),
    path('req_msg/', login_required(views.UpdateReqMsgView.as_view()), name="req_msg"),
    path('my_setting/<user_id>/', login_required(views.MySetting.as_view()), name="my_setting"),
    path('change_password/', login_required(views.ChangePasswordView.as_view()), name="change_password"),
    path('change_chitchat_id/', login_required(views.ChangeChitChatIdView.as_view()), name="change_chitchatId"),
    path('block_list/<user_id>/', login_required(views.BlockListView.as_view()), name="block_list"),
    path('unblock_friend/', login_required(views.UnblockFriendView.as_view()), name="unblock_friend"),
    path('ccid_change_verify/<user_id>/', login_required(views.ChangeCCIDVerify.as_view()), name="ccid_change_verify"),
    path('change_phone/', login_required(views.ChangePhoneNo.as_view()), name="change_phone"),
    path('auth_phone/', login_required(views.AuthenticatePhone.as_view()), name="auth_phone"),
    path('delete_account/', login_required(views.DeleteAccount.as_view()), name="delete_account"),
    path('report/', login_required(views.Report.as_view()), name="report"),
    path('help_and_feedback/', login_required(views.HelpAndFeedback.as_view()), name="help_and_feedback"),
]