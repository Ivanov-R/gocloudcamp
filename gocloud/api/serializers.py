# from django.core.validators import MinValueValidator
from django_filters import rest_framework as filter
from rest_framework import serializers

from .models import Config, ConfigKeyValue, KeyValue

# from rest_framework.validators import UniqueTogetherValidator


class KeySerializer(serializers.ModelSerializer):

    class Meta:
        model = KeyValue
        fields = ('key', 'value')

    # def create(self, validated_data):
    #     print(f'validated_data_k={validated_data}')
    #     data = []
    #     for i in range(len(validated_data)):
    #         data[i] = {'key': validated_data[i].keys(
    #         ), 'value': validated_data[i].values()}
    #     print(data)
    #     return data


class ConfigGetSerializer(serializers.ModelSerializer):
    key_values = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Config
        fields = ('key_values',)
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Favorite.objects.all(),
        #         fields=("user", "favorite_recipe"))]

    def get_key_values(self, obj):
        key_values = KeyValue.objects.filter(config=obj)
        print(key_values)
        data = {}
        for key_value in key_values:
            data[key_value.__dict__['key']] = key_value.__dict__['value']
        return data


class ConfigPostSerializer(serializers.ModelSerializer):
    data = KeySerializer(many=True)

    class Meta:
        model = Config
        fields = ('service', 'data')
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Favorite.objects.all(),
        #         fields=("user", "favorite_recipe"))]

    def create(self, validated_data):
        print(f'validated_data={validated_data}')
        data = validated_data.pop('data')
        print(data)
        config = Config.objects.create(**validated_data)
        print(config)
        for key_value in data:
            new_key_value = KeyValue.objects.create(
                key=key_value['key'], value=key_value['value'],)
            ConfigKeyValue.objects.create(
                config=config, key_value=new_key_value)
        # config.keys.set(keys)
        # print(config)
        return config

    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        config = instance
        for key_value in data:
            try:
                new_key_value = KeyValue.objects.get(key=key_value['key']).update(
                    key=key_value['key'], value=key_value['value'],)
            except:
                new_key_value = KeyValue.objects.create(
                    key=key_value['key'], value=key_value['value'],)
            ConfigKeyValue.objects.update(
                config=config, key_value=new_key_value)
            config.update(version=version+0.1)
        return config
