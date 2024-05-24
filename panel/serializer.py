from rest_framework import serializers

from automation.models import RequestedProductProcessingReport


class RequestedProductProcessingReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestedProductProcessingReport
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['created_by'] = instance.created_by.username
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret

