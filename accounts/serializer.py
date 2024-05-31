from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import Profile, DeliveryProfile, WarehouseProfile, SellerProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Replace None values with empty strings
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        return ret

    class Meta:
        model = Profile
        fields = "__all__"
        depth = 3


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = "__all__"


class WarehouseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProfile
        fields = "__all__"


class DeliveryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryProfile
        fields = "__all__"
