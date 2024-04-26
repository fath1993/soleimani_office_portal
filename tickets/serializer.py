from rest_framework import serializers

from gallery.serializer import FileGallerySerializer
from tickets.models import Message


class MessageSerializer(serializers.ModelSerializer):
    attachments = FileGallerySerializer(many=True)

    class Meta:
        model = Message
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['created_by'] = instance.created_by.username
        return ret
