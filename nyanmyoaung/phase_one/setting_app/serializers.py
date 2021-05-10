from rest_framework import serializers
from setting_app.models import Privacy, SettingNotification, General
from contact_app.models import Contact

""" class AccountSecuritySerializer(serializers.Serializer):
    user = RegisterSerializer()
    id_changed_date = serializers.DateField()
    id_changeable_date = serializers.DateTimeField()
    id_changeable = serializers.BooleanField()
    freeze_account = serializers.BooleanField()
    account_cancellation = serializers.BooleanField()
    
    class Meta:
        model = AccountSecurity
        fields = '__all__' """

class PrivacySerializer(serializers.ModelSerializer):

    class Meta:
        model = Privacy
        exclude = ['user', 'updated_at']

class SettingNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = SettingNotification
        exclude = ['user', 'updated_at']

class GeneralSerializer(serializers.ModelSerializer):

    class Meta:
        model = General
        exclude = ['user', 'updated_at']

class BlockListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user_id', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)
    photo = serializers.ImageField(source='user.photo', read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'name', 'photo']

class SettingSerializer(serializers.Serializer):
    notification = serializers.SerializerMethodField('get_noti')
    privacy =  serializers.SerializerMethodField('get_privacy')
    general =  serializers.SerializerMethodField('get_general')

    def get_noti(self, obj):
        user = self.context.get("user")
        print("===>", user)
        noti_obj = SettingNotification.objects.get_or_create(user=user)
        serializer = SettingNotificationSerializer(noti_obj)
        return serializer.data
        
    def get_privacy(self, obj):
        user = self.context.get("user")
        privacy_obj = Privacy.objects.get_or_create(user=user)
        serializer = PrivacySerializer(privacy_obj)
        return serializer.data

    def get_general(self, obj):
        user = self.context.get("user")
        general_obj = General.objects.get_or_create(user=user)
        serializer = GeneralSerializer(general_obj)
        return serializer.data

    