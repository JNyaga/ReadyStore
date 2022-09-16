from rest_framework.routers import SimpleRouter, DefaultRouter
from django.urls import path, include
from . import views
from pprint import pprint


router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)

# URLConf

urlpatterns = [
    path('', include(router.urls))
]

''' 
[
    # path('products/', views.PoductList.as_view()),
    # path('products/<int:pk>/', views.ProductDescription.as_view()),
    # path('collection/', views.CollectionList.as_view()),
    # # name is the name of the view whichwe want to use in Serializer
    # # we use pk instead of id because we use it in the url
    # path('collections/<int:pk>/', views.CollectionDetail.as_view(),
    #      name='collection-detail'),

]
'''
