"""
Management command para configurar el blog con un solo comando
Ubicación: apps/posts/management/commands/setup_blog.py

Uso: python manage.py setup_blog
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.posts.models import Categoria, Post, Banner
from datetime import datetime, timedelta

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Configura el blog con datos iniciales de SomosKudasai'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando configuración del blog...'))

        # Usar el primer superusuario existente o crear uno si no existe
        self.stdout.write('👤 Verificando usuario administrador...')
        admin = Usuario.objects.filter(is_superuser=True).first()
        
        if admin:
            self.stdout.write(self.style.SUCCESS(f'Usando superusuario existente: {admin.username}'))
        else:
            admin, created = Usuario.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@animeblog.com',
                    'is_staff': True,
                    'is_superuser': True,
                    'first_name': 'Admin',
                    'last_name': 'Blog'
                }
            )
            if created:
                admin.set_password('admin123')
                admin.save()
                self.stdout.write(self.style.SUCCESS('Superusuario admin creado con contraseña: admin123'))
            else:
                self.stdout.write(self.style.WARNING('Usuario admin ya existe'))

        # Crear categorías
        self.stdout.write('Creando categorías...')
        categorias_data = [
            'Anime', 'Manga', 'Noticias', 'Reseñas',
            'Cultura Otaku', 'Novelas Ligeras', 'Videojuegos', 'Estrenos'
        ]
        
        categorias = {}
        for nombre in categorias_data:
            cat, created = Categoria.objects.get_or_create(nombre=nombre)
            categorias[nombre] = cat
            if created:
                self.stdout.write(f'{nombre}')

        # Crear posts
        self.stdout.write('Creando posts con contenido real...')
        posts_data = [
            {
                'titulo': 'My Hero Academia Final Season entra en su etapa de epílogo',
                'categoria': 'Anime',
                'texto': '''La recta final ha comenzado oficialmente. El sitio web del anime Boku no Hero Academia Final Season reveló los detalles del episodio 9, confirmando que la serie entra en su etapa de epílogo. Con solo tres episodios restantes, los fans se preparan para despedirse de esta icónica serie que ha marcado a toda una generación.

El episodio 9 promete ser emotivo y lleno de momentos memorables mientras los héroes enfrentan las consecuencias de la batalla final. La producción ha mantenido un alto nivel de calidad hasta el final, asegurando que la despedida sea digna de esta gran historia.

Los fanáticos de todo el mundo están expresando sus emociones en redes sociales, compartiendo sus momentos favoritos y teorías sobre cómo terminará la historia de Deku y sus compañeros en la U.A.'''
            },
            {
                'titulo': 'Wit Studio anuncia Love Through a Prism, nuevo anime original',
                'categoria': 'Anime',
                'texto': '''Una colaboración de ensueño se ha hecho realidad. Wit Studio ha anunciado la producción de un nuevo anime original titulado Love Through a Prism. La gran noticia es que la historia original y los diseños de personajes provienen de creadores reconocidos en la industria.

Este proyecto marca un nuevo hito para Wit Studio, conocido por sus trabajos en Attack on Titan y Spy x Family. El estudio continúa expandiendo su catálogo con propuestas originales que prometen innovar en el género del romance.'''
            },
            {
                'titulo': 'Girl Crush: El manga sobre K-Pop tendrá adaptación al anime',
                'categoria': 'Anime',
                'texto': '''El mundo del K-Pop recibe un homenaje desde la industria de la animación japonesa. Se ha anunciado oficialmente que el manga Girl Crush, obra de Midori Tayama, tendrá una adaptación al anime para televisión que será transmitida por TBS.

La historia sigue a un grupo de chicas que sueñan con convertirse en ídolos del K-Pop, explorando los desafíos y sacrificios que implica esta industria.'''
            },
            {
                'titulo': 'Chainsaw Man: The Movie Reze Arc - Nuevo tráiler revelado',
                'categoria': 'Estrenos',
                'texto': '''La película Chainsaw Man – The Movie: Reze Arc continúa generando expectativa con nuevo material promocional. Se ha revelado un espectacular tráiler que muestra las intensas secuencias de acción que caracterizarán esta producción de MAPPA.

El arco de Reze es uno de los más esperados por los fans del manga, presentando momentos emocionales y batallas épicas que definirán el futuro de Denji.'''
            },
            {
                'titulo': 'KonoSuba anuncia nuevo OVA para marzo de 2025',
                'categoria': 'Estrenos',
                'texto': '''El sitio oficial de la adaptación al anime de las novelas ligeras KonoSuba ha revelado un nuevo video promocional para el próximo OVA de la franquicia. El video confirma que el estreno está programado para el 14 de marzo en cines de Japón.

Este nuevo OVA promete más de la comedia absurda y las situaciones hilarantes que han hecho de KonoSuba una de las series de comedia fantasy más populares.'''
            },
        ]

        posts_creados = 0
        for i, post_data in enumerate(posts_data):
            post, created = Post.objects.get_or_create(
                titulo=post_data['titulo'],
                defaults={
                    'texto': post_data['texto'],
                    'categoria': categorias[post_data['categoria']],
                    'autor': admin,
                    'activo': True
                }
            )
            if created:
                post.fecha = datetime.now() - timedelta(days=i*2)
                post.save()
                posts_creados += 1
        
        self.stdout.write(self.style.SUCCESS(f' {posts_creados} posts creados'))

        # Crear banners
        self.stdout.write('Creando banners de ejemplo...')
        banners_data = [
            {
                'titulo': 'My Hero Academia Final Season',
                'subtitulo': 'Los últimos episodios están aquí - No te lo pierdas',
                'posicion': 'principal',
                'orden': 1
            },
            {
                'titulo': 'Nuevos Estrenos 2025',
                'subtitulo': 'Descubre los animes más esperados del año',
                'posicion': 'lateral',
                'orden': 1
            },
        ]

        banners_creados = 0
        for banner_data in banners_data:
            banner, created = Banner.objects.get_or_create(
                titulo=banner_data['titulo'],
                defaults={
                    'subtitulo': banner_data['subtitulo'],
                    'posicion': banner_data['posicion'],
                    'orden': banner_data['orden'],
                    'activo': True
                }
            )
            if created:
                banners_creados += 1
        
        self.stdout.write(self.style.SUCCESS(f' {banners_creados} banners creados'))

        # Resumen final
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('¡Configuración completada exitosamente!'))
        self.stdout.write('='*50)
        self.stdout.write(f' Resumen:')
        self.stdout.write(f'   - {Categoria.objects.count()} categorías')
        self.stdout.write(f'   - {Post.objects.count()} posts')
        self.stdout.write(f'   - {Banner.objects.count()} banners')
        self.stdout.write('\n Credenciales de admin:')
        self.stdout.write('   Usuario: admin')
        self.stdout.write('   Contraseña: admin123')
        self.stdout.write('\n Próximos pasos:')
        self.stdout.write('   1. python manage.py runserver')
        self.stdout.write('   2. Ve a http://localhost:8000/admin')
        self.stdout.write('   3. Sube imágenes a los posts y banners')
        self.stdout.write(self.style.SUCCESS('\n ¡Disfruta tu blog de anime!'))