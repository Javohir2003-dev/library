from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user.views import *





urlpatterns = [
    path('user/', user_view, name='user_create'),
    path('profile/',profile_view,name='profile'),
    path('login/', login_view,name='login'),

    path('about/',About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('shop_1', Shop_1.as_view(), name='shop_1'),
    path('shop/', Shop.as_view(), name='shop'),

] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)