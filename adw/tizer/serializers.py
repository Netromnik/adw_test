from rest_framework import serializers
from tizer.models import Wallet, Tizer, Transaction


class TizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tizer
        fields = '__all__'
