from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegistroUsuario

app_name = 'apps.usuario'

urlpatterns = [
    path('registro/', RegistroUsuario.as_view(), name='registro'),
    # Usamos las vistas por defecto de Django para login/logout
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]