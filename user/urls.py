from django.urls import path
from user.views import *


urlpatterns = [
    path('', home,name='home'),
    path('user/', user_view, name='user_url'),
    path('profile/',profile, name='profile_url'),
    path('login/', login_view, name='login_url'),

]