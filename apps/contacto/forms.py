# apps/contacto/forms.py

from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            # Agregamos 'form-control-dark' aquí
            'class': 'form-control form-control-dark', 
            'placeholder': 'Tu nombre completo'
        })
    )
    
    email = forms.EmailField(
        label='Correo Electrónico',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-dark', 
            'placeholder': 'tu.correo@ejemplo.com'
        })
    )
    
    asunto = forms.CharField(
        label='Asunto',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-dark', 
            'placeholder': 'El motivo de tu contacto'
        })
    )
    
    mensaje = forms.CharField(
        label='Mensaje',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-dark', 
            'rows': 5, 
            'placeholder': 'Escribe tu mensaje aquí...',
            'style': 'resize: none;' 
        })
    )