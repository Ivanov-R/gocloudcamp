# from django.core.validators import MinValueValidator
from rest_framework import serializers

from .models import Config, Key

# from rest_framework.validators import UniqueTogetherValidator


class KeySerializer(serializers.ModelSerializer):

    class Meta:
        model = Key
        fields = ('key', 'value')


class ConfigSerializer(serializers.ModelSerializer):
    # key = KeySerializer()

    class Meta:
        model = Config
        fields = ('service', 'version')
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Favorite.objects.all(),
        #         fields=("user", "favorite_recipe"))]

    # def create(self, validated_data):
    #     data = validated_data.pop('data')
    #     config = Config.objects.create(**validated_data)
    #     current_achievement, status = Data.objects.create(
    #         **data)
    #     Config.objects.create(
    #         achievement=current_achievement, cat=cat)
    #     return cat
