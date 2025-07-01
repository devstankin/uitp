from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('netassets.assets.api_urls')),
    path('', include('netassets.assets.urls')),
] 