# apps/posts/models.py
from django.db import models
from django.conf import settings

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Post(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=100)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    imagen = models.ImageField(upload_to='posts', default='static/default_post.jpg', null=True, blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario} en {self.post}'

class Banner(models.Model):
    POSICION_CHOICES = [
        ('principal', 'Banner Principal (Hero)'),
        ('lateral', 'Banner Lateral'),
        ('footer', 'Banner Footer'),
    ]
    
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=300, blank=True, null=True)
    imagen = models.ImageField(upload_to='banners')
    link = models.URLField(blank=True, null=True, help_text="URL a la que redirige el banner")
    posicion = models.CharField(max_length=20, choices=POSICION_CHOICES, default='lateral')
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0, help_text="Orden de aparición (menor número = mayor prioridad)")
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['orden', '-fecha_inicio']
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
    
    def __str__(self):
        return f"{self.titulo} ({self.get_posicion_display()})"