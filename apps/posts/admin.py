from django.contrib import admin
from .models import Post, Categoria, Comentario

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'fecha', 'activo')
    list_filter = ('categoria', 'activo')

admin.site.register(Post, PostAdmin)
admin.site.register(Categoria)
admin.site.register(Comentario)