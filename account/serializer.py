from rest_framework import serializers

from account.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = instance.user.username
        return ret