from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection


# To serialize collections
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title')
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'unit_price',
                  'price_with_tax', 'description', 'collection')
    # Nowwe have to define the fields to serialize in a python dictionary
    # We get the fields from the model that we want to serialize(extenal representation)
    '''
    id = serializers.IntegerField()
    # we define max_length becoz later we will use this field to recieve data from the client(API)
    title = serializers.CharField(max_length=255)
    # source- is the name of the field in the model that we want to serialize
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    # Now our Custom field
'''
    price_with_tax = serializers.SerializerMethodField(
        method_name='get_price_with_tax')
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )

    # We define a method to get the price with tax
    def get_price_with_tax(self, product: Product):
        # Product is the instance of the model
        # Decimal ensures that the value is a decimal for calculations
        return product.unit_price * Decimal(1.1)
