# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]   # Или здесь, или в settings.py
    filterset_fields = ['id', 'title']
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации
    filterset_fields = ['products']
    search_fields = ['products__title', 'products__description']
    ordering_fields = ['id', 'address']
