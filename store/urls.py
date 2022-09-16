from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.PoductList.as_view()),
    path('products/<int:id>/', views.ProductDescription.as_view()),
    path('collection/', views.collection_list),
    # name is the name of the view whichwe want to use in Serializer
    # we use pk instead of id because we use it in the url
    path('collections/<int:pk>/', views.collection_detail,
         name='collection-detail'),

]
