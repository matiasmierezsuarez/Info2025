from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistroUsuarioForm

class RegistroUsuario(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('apps.usuario:login') # Redirige al login tras registrarse