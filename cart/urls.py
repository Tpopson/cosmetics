from django.urls import path 
from .views import *  


app_name = 'cart'

urlpatterns = [
    path('', index, name='shop'),
    path('addtocart', addtocart, name="addtocart"),
    path('mycart', mycart, name="mycart"),
    path('deleteitem', deleteitem, name='deleteitem'),
    path('deletecart', deletecart, name='deletecart'),
    path('decrease', decrease, name='decrease'),
    path('increase', increase, name='increase'),
    path('placeorder', placeorder, name='placeorder'),
    path('checkout', checkout, name='checkout'),
    path('payment', payment, name='payment'),
    path('callback', callback, name='callback'),
]



