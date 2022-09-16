from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection


# To serialize collections
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title', 'products_count')

    products_count = serializers.IntegerField(read_only=True)
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'slug', 'inventory', 'unit_price',
                  'price_with_tax', 'collection')
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


'''     def create(self, validated_data):
        product= Product(**validated_data)
        # -------👇some other field
        product.other=1
        product.save()
        return product
    
    def create(self, instance, validated_data):
        # Instace is the product class
        instance.unit_price = validated_data.get('unit_price')
        instance.save()
        return instance '''


''' 
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            return serializers.ValidationError("Password do not match")
        return data '''
