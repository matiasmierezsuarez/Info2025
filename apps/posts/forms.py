from django import forms
from .models import Post, Comentario

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'texto', 'categoria', 'imagen']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',       # Bootstrap (Responsivo 100% ancho)
                'style': 'resize: none; height: 150px',      # CSS para quitar la esquina de arrastre
                'placeholder': 'Escribe aquí...'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del post'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select mi-select-personalizado',
                'aria-label': 'Selecciona una categoría'
            }),
        }
        

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Escribe tu comentario aquí...'}),
        }