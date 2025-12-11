from django.contrib import admin
from apps.posts.models import Post, Categoria, Comentario, Banner  # IMPORT CORRECTO

class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'fecha', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('titulo', 'texto')
    date_hierarchy = 'fecha'


class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'posicion', 'activo', 'orden', 'fecha_inicio', 'fecha_fin', 'preview_imagen')
    list_filter = ('posicion', 'activo')
    list_editable = ('activo', 'orden')
    search_fields = ('titulo', 'subtitulo')
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'subtitulo', 'imagen', 'link')
        }),
        ('Configuración', {
            'fields': ('posicion', 'activo', 'orden')
        }),
        ('Programación (Opcional)', {
            'fields': ('fecha_inicio', 'fecha_fin'),
            'classes': ('collapse',)
        }),
    )

    def preview_imagen(self, obj):
        if obj.imagen:
            return f'<img src="{obj.imagen.url}" width="100" style="border-radius: 5px;"/>'
        return '❌ Sin imagen'
    preview_imagen.short_description = 'Vista Previa'
    preview_imagen.allow_tags = True


admin.site.register(Post, PostAdmin)
admin.site.register(Categoria)
admin.site.register(Comentario)
admin.site.register(Banner, BannerAdmin)
