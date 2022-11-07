from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

# from .filters import RecipeFilter
from .models import Config
from .serializers import ConfigGetSerializer, ConfigPostSerializer

# class ConfigViewSet(viewsets.ModelViewSet):
#     queryset = Config.objects.all()
#     serializer_class = ConfigGetSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_fields = ('service', 'version')


class APIConfig(APIView):
    def get(self, request):
        data = request.query_params
        # print(f'req_data={data}')
        if 'version' in data.keys():
            config = get_object_or_404(Config,
                                       service=data['service'], version=data['version'])
            serializer = ConfigGetSerializer(config)
            return Response(serializer.data["key_values"])
        configs = Config.objects.filter(service=data['service'])
        # print(f'configs={configs}')
        config = configs.order_by('-version')[0]
        # print(f'config={config}')
        serializer = ConfigGetSerializer(config)
        return Response(serializer.data["key_values"])

    def post(self, request):
        print(f'req_data={request.data}')
        data = request.data
        keys_values_data = data['data']
        # print(f'keys_data={keys_data}')
        new_keys_values_data = []
        # print(f'keys_data.keys={keys_data[0].keys()}')
        # print(f'keys_data.values={keys_data[0].values()}')
        for i in range(len(keys_values_data)):
            # print(i)
            # print(list(keys_data[i].keys()))
            # print(list(keys_data[i].keys())[0])
            # print(list(keys_data[i].values())[0])
            new_dict = {'key': list(keys_values_data[i].keys(
            ))[0], 'value': list(keys_values_data[i].values())[0]}
            # print(new_dict)
            new_keys_values_data.append(new_dict)
        print(f'new_keys_values_data={new_keys_values_data}')
        # print(type(new_keys_data))
        # print(type(data['keys']))
        data['data'] = new_keys_values_data
        print(f'data={data}')
        serializer = ConfigPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(f'ser_err={serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # print(f'req_data={request.data}')
        data = request.data
        configs = Config.objects.filter(service=data['service'])
        # print(f'configs={configs}')
        config = configs.order_by('-version')[0]
        # serializer = CatSerializer(cat, data=request.data)
        keys_values_data = data['data']
        # print(f'keys_data={keys_data}')
        new_keys_values_data = []
        # print(f'keys_data.keys={keys_data[0].keys()}')
        # print(f'keys_data.values={keys_data[0].values()}')
        for i in range(len(keys_values_data)):
            # print(i)
            # print(list(keys_data[i].keys()))
            # print(list(keys_data[i].keys())[0])
            # print(list(keys_data[i].values())[0])
            new_dict = {'key': list(keys_values_data[i].keys(
            ))[0], 'value': list(keys_values_data[i].values())[0]}
            # print(new_dict)
            new_keys_values_data.append(new_dict)
        print(f'new_keys_values_data={new_keys_values_data}')
        # print(type(new_keys_data))
        # print(type(data['keys']))
        data['data'] = new_keys_values_data
        print(f'data={data}')
        serializer = ConfigPostSerializer(config, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(f'ser_err={serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        ...

    def delete(self, request):
        ...
