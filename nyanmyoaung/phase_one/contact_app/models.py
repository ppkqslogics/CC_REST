from django.db import models
from profile_app.models import Profile
from userapp.id_generator import tag_id_generator
from userapp.models import User


def unique_tag_id():
    unique_id = tag_id_generator()
    try:
        while TagsModel.objects.filter(tag_id=unique_id).exists():
            unique_id = tag_id_generator()
        return unique_id
    except Exception:
        return unique_id


class Contact(models.Model):
    """
    Contact model for user \n
    INPUT : friends_list, block_list \n
    OUTPUT : friends_list, block_list \n
    RETURN : user name, friends lists, friends values, friends count \n
    Note : need to configure block_list
    """
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    friends = models.ManyToManyField(
        Profile, related_name='friends_list', through='FriendsModel', blank=True)
    block_list = models.ManyToManyField(
        Profile, related_name='block_list', blank=True)

    def __str__(self):
        return str(self.user)

    def get_friends(self):
        return self.friends.all()

    def get_friends_values(self):
        return self.friends.values()

    def get_friends_no(self):
        return self.friends.all().count()

    """ def get_block_list(self):
        return self.block_list.all() """


class FriendsModel(models.Model):
    """
    Model for friends list through this model for contact \n
    INPUT : owner, friend, nick_name, creted_at, updated_at \n
    OUTPUT : friend list through contact \n
    RETURN : owner name - friend name
    """
    owner = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True)
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    nick_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner}-{self.friend}"

    class Meta:
        unique_together = ["owner", "friend"]


class TagsModel(models.Model):
    """
    Tag model for tagged person \n
    INPUT : tag_id, tag_name, owner, tagged_member(id, id, id) \n
    OUTPUT : tag_lists \n
    RETURN : tag_name
    """
    tag_id = models.CharField(max_length=8, default=unique_tag_id, unique=True)
    tag_name = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True)
    tagged_member = models.ManyToManyField(Profile, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return str(self.tag_name)

    class Meta:
        unique_together = ["owner", "tag_name"]


class Relationship(models.Model):
    """
    Relationship status for user \n
    INPUT : message, sender, receiver, status(auto added) \n
    OUTPUT : relation lists \n
    RETURN : sender_name-receiver_name
    """
    request_message = models.CharField(max_length=20, blank=True)
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

    class Meta:
        unique_together = ["receiver", "sender"]
