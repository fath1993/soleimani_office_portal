from rest_framework import serializers

from accounts.serializer import ProfileSerializer
from automation.models import RequestedProductProcessingReport, Customer, CreditCard
from resource.serializer import ProductSerializer


class CreditCardSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer()
    brokers = ProfileSerializer(many=True)

    class Meta:
        model = CreditCard
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        ret['updated_at'] = instance.updated_at.strftime('%Y-%m-%d ساعت %H:%M')
        ret['created_by'] = instance.created_by.username
        ret['updated_by'] = instance.updated_by.username
        return ret


class CustomerSerializer(serializers.ModelSerializer):
    desired_product = ProductSerializer(many=True)

    class Meta:
        model = Customer
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret


class RequestedProductProcessingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedProductProcessingReport
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['created_by'] = instance.created_by.username
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret
