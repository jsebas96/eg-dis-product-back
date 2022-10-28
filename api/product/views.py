from typing import OrderedDict
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer
from .models import Product
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from math import ceil


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_query_param = 'page'

    def get_paginated_response(self, data):
        headers = {
            'Access-Control-Allow-Origin': '*'
        }
        return Response(
            {'info': OrderedDict([('count', ceil(self.page.paginator.count / self.page_size)), ('next', self.get_next_link()), ('previous', self.get_previous_link())]), 'results': data}, headers=headers
        )


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.all().order_by('-createdDate')
        if len(queryset) == 0:
            return Response({'message': 'no hay productos'}, status=status.HTTP_404_NOT_FOUND)
        page = self.paginate_queryset(queryset)
        serializer = ProductSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        headers = {
            'Access-Control-Allow-Origin': '*',
        }
        print(request.data)
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, pk=None):
        headers = {
            'Access-Control-Allow-Origin': '*',
        }
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        if not product:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND, headers=headers)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def update(self, request, pk=None):
        headers = {
            'Access-Control-Allow-Origin': '*',
        }
        product = get_object_or_404(Product, pk=pk)
        if product:
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data, headers=headers)
        return Response({'message': 'producto no encontrado'}, status=status.HTTP_404_BAD_REQUEST, headers=headers)

    def destroy(self, request, pk=None):
        headers = {
            'Access-Control-Allow-Origin': '*',
        }
        product = get_object_or_404(Product, pk=pk)
        if product:
            serializer = ProductSerializer(product)
            product.delete()
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        return Response({'message': 'producto no encontrado'}, status=status.HTTP_404_BAD_REQUEST, headers=headers)
