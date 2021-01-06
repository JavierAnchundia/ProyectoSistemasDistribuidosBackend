from django.contrib import admin
from django.urls import path, include
from serviciosBackend import urls
from django.conf.urls.static import static
from django.conf import settings
from ServidorMapaVirtual import views
from rest_framework import routers
from serviciosBackend.views import UserViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/', include(urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # vista para mostrar form de cambiar contraseña  10/11/2020
    path('recuperar_password/_9d_us5r_=/<int:id_user>/<str:token>/', views.RecuperarContrasena),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
