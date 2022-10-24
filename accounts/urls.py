from django.urls import path
from .views import * 

app_name = 'accounts'

urlpatterns = [
    path('', account, name='accounts'),
    path('signout', signout, name='signout'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('profile', profile, name='profile'),
    path('profile_update', profile_update, name='profile_update'),
    path('password', change_password, name='password'),
    path('password_reset', password_reset_request, name='password_reset'),
]
