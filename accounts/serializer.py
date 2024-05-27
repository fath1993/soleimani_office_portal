from rest_framework import serializers

from accounts.models import Profile
from automation.models import RequestedProductProcessingReport, Customer
from portal.models import Product


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"
        depth = 3

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret
