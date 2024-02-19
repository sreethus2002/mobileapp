from rest_framework import serializers
from mobile.models import Mobiles

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mobiles
        fields="__all__"
