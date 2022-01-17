from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
    path('admin/', admin.site.urls),
    
    re_path(r'api/events?/', include('events.urls'), name='events'),
    re_path(r'api/locations?/', include('locations.urls'), name='locations'),
    re_path(r'api/posts?/', include('posts.urls'), name='posts'),
    path('api/user/', include('users.urls'), name='users'),    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
