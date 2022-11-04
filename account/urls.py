from django.urls import path, include
from .views import *

urlpatterns = [
     # Account Urls
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logoutUser, name="logout"),
    path('', include('django.contrib.auth.urls')),
]