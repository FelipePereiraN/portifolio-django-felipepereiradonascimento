from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('polls/', include('polls.urls')),
    path('portfolio/', include('portfolio.urls')),

    # API de Tarefas (da aula DRF)
    path('api/tarefas/', include('tarefas.urls')),

    # API do Perfil
    path('', include('core.urls')),

    # Autenticacao JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]