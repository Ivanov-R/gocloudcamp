from rest_framework import serializers

from .models import Config, ConfigKeyValue, KeyValue


class KeySerializer(serializers.ModelSerializer):

    class Meta:
        model = KeyValue
        fields = ('key', 'value')


class ConfigGetSerializer(serializers.ModelSerializer):
    key_values = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Config
        fields = ('key_values',)

    def get_key_values(self, obj):
        key_values = KeyValue.objects.filter(config=obj)
        data = {}
        for key_value in key_values:
            data[key_value.__dict__['key']] = key_value.__dict__['value']
        return data


class ConfigPostSerializer(serializers.ModelSerializer):
    data = KeySerializer(many=True)

    class Meta:
        model = Config
        fields = ('service', 'data')

    def create(self, validated_data):
        data = validated_data.pop('data')
        config = Config.objects.create(**validated_data)
        for key_value in data:
            new_key_value, _ = KeyValue.objects.get_or_create(
                key=key_value['key'], value=key_value['value'],)
            ConfigKeyValue.objects.create(
                config=config, key_value=new_key_value)
        return config

    def update(self, instance, validated_data):
        data = validated_data.pop('data')
        config = instance
        for key_value in data:
            new_key_value = KeyValue.objects.filter(
                key=key_value['key'], value=key_value['value'])
            if not new_key_value or not ConfigKeyValue.objects.filter(
                    config=config, key_value=new_key_value[0]):
                config, _ = Config.objects.get_or_create(
                    service=config.service, version=(config.version +
                                                     int('1')))
                break
        for key_value in data:
            new_key_value, _ = KeyValue.objects.get_or_create(
                key=key_value['key'], value=key_value['value'])
            if not ConfigKeyValue.objects.filter(
                    config=config, key_value=new_key_value).exists():
                ConfigKeyValue.objects.create(
                    config=config, key_value=new_key_value)
        return config
