from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from book.views import Index





urlpatterns = [
    path('', Index.as_view(), name='index'),
    

] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)