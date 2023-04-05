from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from django.urls import path, include
from . import views
from pprint import pprint


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename="products")
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
# pprint(router.urls)

# Child router
product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
# Basename-> used as prefix for generating url patterns
product_router.register('reviews', views.ReviewViewset,
                        basename='product-reviews')
product_router.register(
    'images', views.ProductImageViewSet, basename='product-images')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')

carts_router.register('items', views.CartItemViewSet, basename='cart-items')


# pprint(product_router.urls)


# URLConf

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(carts_router.urls)),
]
