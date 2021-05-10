from django.db.models.signals import post_save
from django.dispatch import receiver
from userapp.models import User
from profile_app.models import Profile
from contact_app.models import Contact
from setting_app.models import Privacy

@receiver(post_save, sender=User)
def post_save_create_data(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # AccountSecurity.objects.create(user=instance)
        # Privacy.objects.create(user=instance)
        # General.objects.create(user=instance)
        # Notifications.objects.create(user=instance)
        Contact.objects.create(user=instance)
        Privacy.objects.create(user=instance)

""" @receiver(post_save, sender=Relationship)
def post_save_add_to_friend(sender, created, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    print(sender,receiver)
    if instance.status == 'accepted':
        sender.friend.add(receiver.user)
        receiver.friend.add(sender.user)
        sender.save()
        receiver.save() """