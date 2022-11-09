from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Config
from .serializers import ConfigGetSerializer, ConfigPostSerializer


class APIConfig(APIView):
    def get(self, request):
        data = request.query_params
        if "version" in data.keys():
            config = get_object_or_404(
                Config, service=data["service"], version=data["version"]
            )
            serializer = ConfigGetSerializer(config)
            return Response(serializer.data["key_values"])
        configs = Config.objects.filter(service=data["service"])
        if configs.exists():
            config = configs.order_by("-version")[0]
            serializer = ConfigGetSerializer(config)
            return Response(serializer.data["key_values"])
        return Response(
            "Такого конфига не существует! Воспользуйтесь методом Post, чтобы"
            " создать конфиг для этого приложения",
            status=status.HTTP_404_NOT_FOUND,
        )

    def post(self, request):
        data = request.data
        if "service" in data.keys():
            if Config.objects.filter(service=data["service"]).exists():
                return Response(
                    "Такой конфиг уже существует! Воспользуйтесь методом Put,"
                    " чтобы добавить новую версию для этого приложения",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        keys_values_data = data["data"]
        new_keys_values_data = []
        for i in range(len(keys_values_data)):
            new_dict = {
                "key": list(keys_values_data[i].keys())[0],
                "value": list(keys_values_data[i].values())[0],
            }
            new_keys_values_data.append(new_dict)
        data["data"] = new_keys_values_data
        serializer = ConfigPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        configs = Config.objects.filter(service=data["service"])
        if configs.exists():
            config = configs.order_by("-version")[0]
            keys_values_data = data["data"]
            new_keys_values_data = []
            for i in range(len(keys_values_data)):
                new_dict = {
                    "key": list(keys_values_data[i].keys())[0],
                    "value": list(keys_values_data[i].values())[0],
                }
                new_keys_values_data.append(new_dict)
            data["data"] = new_keys_values_data
            serializer = ConfigPostSerializer(config, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            "Такого конфига не существует! Воспользуйтесь методом Post, чтобы"
            " создать конфиг для этого приложения",
            status=status.HTTP_404_NOT_FOUND,
        )

    def delete(self, request):
        data = request.query_params
        if data["service"] == "":
            config = get_object_or_404(
                Config, service="", version=data["version"]
            )
            config.delete()
            return Response(
                "Версия конфига успешно удалена",
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            "Нельзя удалять конфиг, который используется каким-либо"
            " приложением!",
            status=status.HTTP_400_BAD_REQUEST,
        )
