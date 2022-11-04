from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from online_admission.settings import STATIC_ROOT

urlpatterns = [
    path('user/', admin.site.urls),
    path('', include('admission.urls')),
    path('accounts/', include('account.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
