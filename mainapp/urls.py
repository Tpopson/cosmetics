from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('categories', categories, name='categories'),
    path('category/<str:id>/<slug:slug>', category, name='category'),
    path('products', products, name='products'),
    path('details/<str:id>/<slug:slug>', product_details, name='details'),
]
