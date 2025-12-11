from django.urls import path
from .views import contacto, contacto_gracias

app_name = 'apps.contacto'

urlpatterns = [
    path('', contacto, name='contacto'),
    path('gracias/', contacto_gracias, name='contacto_gracias'),
]