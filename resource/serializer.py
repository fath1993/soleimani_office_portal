from django.urls import reverse
from rest_framework import serializers
from resource.models import Product, TeaserMaker, ResellerNetwork, AdvertiseContent, ForwardToPortal, \
    CommunicationChannel, Registrar, Receiver
from soleimani_office_portal.settings import BASE_URL
from gallery.serializer import FileGallerySerializer


class ProductSerializer(serializers.ModelSerializer):
    images = FileGallerySerializer(many=True)
    videos = FileGallerySerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):

        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        # ret['link'] = f'{BASE_URL}{reverse("resource:product-detail-with-id", kwargs={"product_id": f"{instance.id}"})}'.replace('//', '/')
        ret['created_by'] = instance.created_by.username
        ret['updated_by'] = instance.updated_by.username
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        ret['updated_at'] = instance.updated_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret


class TeaserMakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeaserMaker
        fields = "__all__"

    def to_representation(self, instance):

        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        ret['created_by'] = instance.created_by.username
        ret['updated_by'] = instance.updated_by.username
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        ret['updated_at'] = instance.updated_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret


class ResellerNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResellerNetwork
        fields = "__all__"

    def to_representation(self, instance):

        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        ret['created_by'] = instance.created_by.username
        ret['updated_by'] = instance.updated_by.username
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        ret['updated_at'] = instance.updated_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret


class ReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiver
        fields = "__all__"

    def to_representation(self, instance):

        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        ret['created_by'] = instance.created_by.username
        ret['updated_by'] = instance.updated_by.username
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        ret['updated_at'] = instance.updated_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret


class AdvertiseContentSerializer(serializers.ModelSerializer):
    content = FileGallerySerializer(many=True)
    class Meta:
        model = AdvertiseContent
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):

        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        ret['created_by'] = instance.created_by.username
        ret['updated_by'] = instance.updated_by.username
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        ret['updated_at'] = instance.updated_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret


class ForwardToPortalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForwardToPortal
        fields = "__all__"

    def to_representation(self, instance):

        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        ret['created_by'] = instance.created_by.username
        ret['updated_by'] = instance.updated_by.username
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        ret['updated_at'] = instance.updated_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret


class CommunicationChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationChannel
        fields = "__all__"

    def to_representation(self, instance):

        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        ret['created_by'] = instance.created_by.username
        ret['updated_by'] = instance.updated_by.username
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        ret['updated_at'] = instance.updated_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret


class RegistrarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registrar
        fields = "__all__"

    def to_representation(self, instance):

        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        ret['created_by'] = instance.created_by.username
        ret['updated_by'] = instance.updated_by.username
        ret['created_at'] = instance.created_at.strftime('%Y-%m-%d ساعت %H:%M')
        ret['updated_at'] = instance.updated_at.strftime('%Y-%m-%d ساعت %H:%M')
        return ret