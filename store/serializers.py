from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection, Review, Cart, CartItem, Customer


# To serialize collections


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
'''
    # Now our Custom field
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


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title', 'products_count')

    products_count = serializers.IntegerField(read_only=True)
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serilizers.ValidationError(
                "No product with given ID was found")

        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            # Updating an existing cart item
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # Create a new cart item
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']
