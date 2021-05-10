from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Contact
    path('add_friend/', login_required(views.FriendRequestView.as_view(), login_url = 'another'), name="friend_profile"),
    path('confirm_friend/', login_required(views.ConfirmFriendView.as_view(), login_url = 'another'), name="confirm_friend"),
    path('friend_request/<user_id>/', login_required(views.ReceiverView.as_view(), login_url = 'another'), name="friend_request"),
    path('friend_list/<user_id>/', login_required(views.FriendListView.as_view(), login_url = 'another'), name="friend_list"),
    
    # Tag
    path('add_tag/', login_required(views.TagsView.as_view(), login_url = 'another'), name="add_tag"),
    # Findfriend
    path('find_friend/', login_required(views.FindFriendView.as_view(), login_url = 'another'), name="find_friend"),
    path('contact_upload/', login_required(views.ContactUpload.as_view(), login_url = 'another'), name="contact_upload"),
    path('delete_contact/', login_required(views.DeleteContact.as_view(), login_url = 'another'), name="delete_contact"),
    path('edit_contact/', login_required(views.EditContact.as_view(), login_url = 'another'), name="edit_contact"),
    # Tagsview
    path('edit_contact_all_tag/<user_id>/<friend_id>/', login_required(views.EditContactAllTags.as_view(), login_url = 'another'), name="edit_contact_all_tag"),
    path('edit_contact_tag/<user_id>/<friend_id>/', login_required(views.EditContactTag.as_view(), login_url = 'another'), name="edit_contact_tag"),
    path('edit_contact_add_tag/', login_required(views.EditContactAddTag.as_view(), login_url = 'another'), name="edit_contact_add_tag"),
    path('tag/', login_required(views.TagsView.as_view(), login_url = 'another'), name="tag"),
    path('tag_list/<user_id>/', login_required(views.TagsListView.as_view(), login_url = 'another'), name="tag_list"),
    path('delete_tag/', login_required(views.TagDeleteView.as_view(), login_url = 'another'), name="delete_tag"),
    #Block
    path('block_friend/', login_required(views.FriendBlockView.as_view(), login_url = 'another'), name="block_friend"),
]