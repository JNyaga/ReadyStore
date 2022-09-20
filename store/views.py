from django.db.models.aggregates import Count
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Product, Collection, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer
# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({"error": "Product cannot be deleted because it is associated with an order"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


''' @api_view(['GET', 'POST'])
def product_list(request):
    # 👇
    if request.method == 'GET':
        # select_related helps us to avoid N+1 queries
        # It speeds up the query by selecting the related fields
        queryset = Product.objects.select_related('collection').all()
        # many=True means that we are sending many products
        # context is passed on to the serializer since it needs to know the url of the collection
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        # to desirilize the data we pass our data to our product serializer
        serializer = ProductSerializer(
            data=request.data, context={"request":  request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 '''


''' 
@api_view(['GET', 'PUT', 'DELETE'])
def product_description(request, id):
    # here we pass 2 arguments 1.type of model
    # and 2.lookup id
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        # create a serializer to seri alize the product
        serializer = ProductSerializer(product, context={"request": request})
        # the above gives a dictionary of the product
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(
            product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        # To handle foreign key protected  in orderitem
        if product.orderitems.count() > 0:
            return Response({"error": "Product cannot be deleted because it is associated with an order"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) '''


''' @api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) '''


''' @api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    # We use pk since django rest framework uses it to lookup the object and we use it in the url
    collection = get_object_or_404(Collection.objects.annotate(
        products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) '''


class ReviewViewset(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
