import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogAnime.configuraciones.settings')
django.setup()

from apps.posts.models import Categoria, Post, Banner
from apps.usuario.models import Usuario
from datetime import datetime, timedelta

print("=" * 60)
print("INICIANDO POBLADO DE BASE DE DATOS")
print("=" * 60)

# Usar el primer superusuario existente o crear uno si no existe
try:
    admin = Usuario.objects.filter(is_superuser=True).first()
    if admin:
        print(f"Usando superusuario existente: {admin.username}")
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
            print("Usuario admin creado con contraseña: admin123")
except Exception as e:
    print(f"Error al obtener usuario: {e}")
    print("Los posts se crearán sin autor")
    admin = None

# Crear categorías
print("\n Creando categorías...")
categorias_data = [
    'Anime',
    'Manga',
    'Noticias',
    'Reseñas',
    'Cultura Otaku',
    'Novelas Ligeras',
    'Videojuegos',
    'Estrenos'
]

categorias = {}
for nombre in categorias_data:
    cat, created = Categoria.objects.get_or_create(nombre=nombre)
    categorias[nombre] = cat
    if created:
        print(f"Categoría creada: {nombre}")

# Posts con contenido real de Kudasai
print("\n Creando posts...")
posts_data = [
    {
        'titulo': 'My Hero Academia Final Season entra en su etapa de epilogo',
        'categoria': 'Anime',
        'texto': 'La recta final ha comenzado oficialmente. El sitio web del anime Boku no Hero Academia Final Season revelo los detalles del episodio 9, confirmando que la serie entra en su etapa de epilogo. Con solo tres episodios restantes, los fans se preparan para despedirse de esta iconica serie que ha marcado a toda una generacion.\n\nEl episodio 9 promete ser emotivo y lleno de momentos memorables mientras los heroes enfrentan las consecuencias de la batalla final. La produccion ha mantenido un alto nivel de calidad hasta el final, asegurando que la despedida sea digna de esta gran historia.\n\nLos fanaticos de todo el mundo estan expresando sus emociones en redes sociales, compartiendo sus momentos favoritos y teorias sobre como terminara la historia de Deku y sus companeros en la U.A.'
    },
    {
        'titulo': 'Wit Studio anuncia Love Through a Prism, nuevo anime original',
        'categoria': 'Anime',
        'texto': 'Una colaboracion de ensueno se ha hecho realidad. Wit Studio ha anunciado la produccion de un nuevo anime original titulado Love Through a Prism. La gran noticia es que la historia original y los disenos de personajes provienen de creadores reconocidos en la industria.\n\nEste proyecto marca un nuevo hito para Wit Studio, conocido por sus trabajos en Attack on Titan y Spy x Family. El estudio continua expandiendo su catalogo con propuestas originales que prometen innovar en el genero del romance.\n\nLos primeros visuales revelados muestran un estilo artistico refinado y vibrante, caracteristico de las producciones de Wit Studio. La comunidad anime ya espera con ansias mas detalles sobre la trama y fecha de estreno.'
    },
    {
        'titulo': 'Girl Crush: El manga sobre K-Pop tendra adaptacion al anime',
        'categoria': 'Anime',
        'texto': 'El mundo del K-Pop recibe un homenaje desde la industria de la animacion japonesa. Se ha anunciado oficialmente que el manga Girl Crush, obra de Midori Tayama, tendra una adaptacion al anime para television que sera transmitida por TBS.\n\nLa historia sigue a un grupo de chicas que suenan con convertirse en idolos del K-Pop, explorando los desafios y sacrificios que implica esta industria. El manga ha ganado popularidad por su representacion realista del mundo del entretenimiento coreano.\n\nEsta adaptacion representa un puente cultural interesante entre Japon y Corea, dos potencias del entretenimiento asiatico. Los fans de ambos paises ya celebran este anuncio que promete unir lo mejor de ambas industrias.'
    },
    {
        'titulo': 'Chainsaw Man: The Movie Reze Arc - Nuevo trailer revelado',
        'categoria': 'Estrenos',
        'texto': 'La pelicula Chainsaw Man - The Movie: Reze Arc continua generando expectativa con nuevo material promocional. Se ha revelado un espectacular trailer que muestra las intensas secuencias de accion que caracterizaran esta produccion de MAPPA.\n\nEl arco de Reze es uno de los mas esperados por los fans del manga, presentando momentos emocionales y batallas epicas que definiran el futuro de Denji. La animacion mostrada en el trailer mantiene el alto nivel de calidad que caracterizo a la primera temporada.\n\nLos espectadores en Japon recibiran beneficios especiales por asistir a las primeras proyecciones, incluyendo ilustraciones exclusivas y merchandise limitado. El estreno promete ser uno de los eventos anime mas importantes del ano.'
    },
    {
        'titulo': 'Samurai Troopers regresa con Yoroi Shin Den',
        'categoria': 'Noticias',
        'texto': 'Los guerreros con armadura mistica estan de vuelta para proteger el mundo moderno. El equipo de produccion de Yoroi Shin Den Samurai Troopers ha confirmado detalles sobre la nueva secuela del clasico anime.\n\nEsta nueva iteracion promete modernizar la franquicia manteniendo los elementos que la hicieron memorable en los anos 80 y 90. Los fans nostalgicos podran revivir la emocion de las batallas epicas con armaduras legendarias.\n\nEl proyecto ha generado gran entusiasmo entre la comunidad anime, especialmente entre aquellos que crecieron viendo la serie original. Las primeras imagenes revelan un diseno actualizado que respeta la estetica clasica.'
    },
    {
        'titulo': 'Prime Video bajo fuego por usar IA para doblar Banana Fish',
        'categoria': 'Noticias',
        'texto': 'Lo que muchos temian ha comenzado a suceder en una de las plataformas mas grandes del mundo. Prime Video se encuentra actualmente en el ojo del huracan tras descubrirse que esta utilizando Inteligencia Artificial para doblar series de anime, especificamente Banana Fish.\n\nLos fans han expresado su indignacion en redes sociales, argumentando que el doblaje con IA no puede capturar las emociones y matices que los actores de voz profesionales aportan a los personajes. La controversia ha reavivado el debate sobre el uso de IA en la industria del entretenimiento.\n\nEste caso podria sentar un precedente importante sobre como las plataformas de streaming manejan el contenido anime. La comunidad exige respeto por el trabajo de los profesionales de la voz y la preservacion de la calidad artistica.'
    },
    {
        'titulo': 'TOHO anuncia nueva serie anime de Godzilla',
        'categoria': 'Estrenos',
        'texto': 'La franquicia del Rey de los Monstruos esta lista para romper sus propias reglas. Durante el Anime Festival Asia Singapore 2025, TOHO animation revelo una nueva serie de anime de Godzilla que promete redefinir la franquicia.\n\nEste proyecto explorara nuevas narrativas dentro del universo de Godzilla, ofreciendo una perspectiva fresca sobre el iconico kaiju. Los detalles sobre la trama aun se mantienen en secreto, pero las primeras imagenes conceptuales muestran un enfoque visualmente impactante.\n\nLa serie busca atraer tanto a fans veteranos como a nuevas audiencias, combinando la esencia clasica de Godzilla con tecnicas de animacion modernas. TOHO ha demostrado su compromiso con la calidad en proyectos animados anteriores.'
    },
    {
        'titulo': 'World Trigger lanza misterioso mensaje sobre REBOOT',
        'categoria': 'Noticias',
        'texto': 'La comunidad de World Trigger esta en alerta maxima. La cuenta oficial del anime lanzo un visual misterioso que simplemente dice "12.4 REBOOT", sugiriendo un anuncio importante para el 4 de diciembre.\n\nLas especulaciones abundan sobre que podria significar este "REBOOT". Se trata de una nueva temporada? Un remake? O quizas una pelicula? Los fans analizan cada detalle del visual buscando pistas sobre el futuro de la serie.\n\nWorld Trigger ha mantenido una base de fans leales a pesar de los desafios de produccion en el pasado. Este anuncio genera esperanza de que la franquicia continuara con nuevo contenido de calidad.'
    },
    {
        'titulo': 'Kimetsu no Yaiba invade Japon con anuncios gigantes de Shinobu',
        'categoria': 'Cultura Otaku',
        'texto': 'Si caminas por las calles de Tokio u Osaka hoy, es muy probable que te encuentres con la sonrisa gigante de Shinobu Kocho. A partir del 1 de diciembre, han comenzado a aparecer anuncios publicitarios a gran escala de Demon Slayer en las principales ciudades de Japon.\n\nEstos impresionantes anuncios promocionan la proxima temporada y productos relacionados con la franquicia. Shinobu, uno de los personajes mas queridos por los fans, es la protagonista de esta campana masiva.\n\nLa estrategia de marketing de Kimetsu no Yaiba continua siendo agresiva y efectiva, manteniendo la serie en el ojo publico incluso entre temporadas. Los fans comparten fotografias de los anuncios en redes sociales, creando viralidad organica.'
    },
    {
        'titulo': 'KonoSuba anuncia nuevo OVA para marzo de 2025',
        'categoria': 'Estrenos',
        'texto': 'El sitio oficial de la adaptacion al anime de las novelas ligeras KonoSuba ha revelado un nuevo video promocional para el proximo OVA de la franquicia. El video confirma que el estreno esta programado para el 14 de marzo en cines de Japon.\n\nEste nuevo OVA promete mas de la comedia absurda y las situaciones hilarantes que han hecho de KonoSuba una de las series de comedia fantasy mas populares. Kazuma y su disfuncional grupo de aventureros regresan para mas desventuras.\n\nTras el lanzamiento en cines, el OVA estara disponible en plataformas de streaming para audiencias internacionales. Los fans alrededor del mundo esperan con ansias mas contenido de esta querida serie.'
    },
    {
        'titulo': 'Katekyo Hitman Reborn podria regresar con nuevo anime',
        'categoria': 'Noticias',
        'texto': 'Las redes sociales y foros otaku se han encendido con una filtracion que apunta al regreso de uno de los shonen mas queridos de los 2000. Se ha detectado el registro de un nuevo dominio web vinculado a Pony Canyon.\n\nEste tipo de movimientos suelen preceder confirmaciones oficiales de nuevas temporadas o remakes. El manga original dejo varios arcos sin animar cuando la serie termino en 2010, incluyendo el muy esperado arco final.\n\nLos fans especulan si sera una continuacion directa o un reboot completo con animacion moderna. Katekyo Hitman Reborn marco a toda una generacion con su mezcla de comedia y accion shonen.'
    },
    {
        'titulo': 'Sony lanzara criptomoneda para pagos de anime y juegos',
        'categoria': 'Cultura Otaku',
        'texto': 'Sony ha anunciado planes para lanzar su propia criptomoneda estable especificamente disenada para transacciones relacionadas con anime, manga y videojuegos. Esta iniciativa busca facilitar las compras digitales en el ecosistema de entretenimiento.\n\nLa criptomoneda de Sony permitira a los fans comprar merchandise, acceder a contenido premium y participar en eventos virtuales de manera mas eficiente. El gigante japones apuesta por la tecnologia blockchain para revolucionar la industria.\n\nEste movimiento refleja como las grandes companias estan adoptando tecnologias emergentes para mejorar la experiencia del consumidor. La comunidad otaku observa con interes como se desarrollara esta iniciativa.'
    },
    {
        'titulo': 'Polemica: Boton de saltar opening genera debate en Japon',
        'categoria': 'Cultura Otaku',
        'texto': 'Una acalorada discusion ha surgido en la comunidad anime japonesa sobre la funcion de saltar opening en plataformas de streaming. Muchos creadores y fans puristas consideran que esta opcion falta al respeto al trabajo de los artistas.\n\nLos openings de anime son considerados parte integral de la experiencia artistica, con equipos dedicados que invierten tiempo y recursos en crear secuencias memorables. Saltarlos, argumentan algunos, es como saltarse el prologo de una pelicula.\n\nPor otro lado, defensores de la funcion senalan la conveniencia para maratones y la libertad de eleccion del espectador. El debate refleja tensiones mas amplias sobre como el consumo digital esta cambiando las tradiciones culturales.'
    },
    {
        'titulo': 'Now That We Draw: Manga confirmado para adaptacion anime',
        'categoria': 'Anime',
        'texto': 'Una nueva comedia romantica esta lista para dar el salto a la television. El manga Kakunaru Ue wa ha sido confirmado para recibir una adaptacion al anime por el estudio ROLL2.\n\nLa historia sigue a dos aspirantes a mangaka que deciden iniciar una relacion falsa para usar como referencia en sus obras romanticas. La premisa meta y las situaciones comicas que genera han conquistado a los lectores del manga.\n\nEl elenco de voces incluye a Sayumi Suzushiro y Ayumu Murase como los protagonistas. Los fans del manga esperan que la adaptacion capture el encanto y humor que hace especial a esta serie.'
    },
    {
        'titulo': 'Tomomichi Nishimura, legendaria voz del anime, fallece',
        'categoria': 'Noticias',
        'texto': 'Una voz inconfundible que marco a generaciones de fans del anime y videojuegos se ha apagado. La agencia Arts Vision anuncio el fallecimiento del veterano actor de voz Tomomichi Nishimura, ocurrido el pasado 29 de noviembre.\n\nNishimura-san presto su voz a innumerables personajes memorables a lo largo de decadas de carrera, desde series clasicas hasta producciones modernas. Su voz profunda y distintiva era instantaneamente reconocible para los fans.\n\nLa industria del anime y la comunidad de fans rinden homenaje a este gran profesional. Su legado perdurara en las obras que ayudo a dar vida y en los corazones de quienes crecieron escuchando su voz.'
    }
]

# Crear posts
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
        print(f"Post creado: {post_data['titulo'][:50]}...")

# Crear banners de ejemplo
print("\n Creando banners...")
banners_data = [
    {
        'titulo': 'My Hero Academia Final Season',
        'subtitulo': 'Los ultimos episodios estan aqui - No te lo pierdas',
        'posicion': 'principal',
        'orden': 1
    },
    {
        'titulo': 'Chainsaw Man Movie',
        'subtitulo': 'El Arco de Reze llega a la pantalla grande',
        'posicion': 'principal',
        'orden': 2
    },
    {
        'titulo': 'Nuevos Estrenos 2025',
        'subtitulo': 'Descubre los animes mas esperados del ano',
        'posicion': 'lateral',
        'orden': 1
    },
    {
        'titulo': 'Resenas Exclusivas',
        'subtitulo': 'Analisis profundos de tus series favoritas',
        'posicion': 'lateral',
        'orden': 2
    }
]

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
        print(f"Banner creado: {banner_data['titulo']}")

print("\n" + "=" * 60)
print(" BASE DE DATOS POBLADA EXITOSAMENTE")
print("=" * 60)
print(f"\n📊 Resumen:")
print(f"   - {Categoria.objects.count()} categorias")
print(f"   - {Post.objects.count()} posts")
print(f"   - {Banner.objects.count()} banners")
if admin and admin.username == 'admin':
    print(f"\n Credenciales de admin:")
    print(f"   Usuario: admin")
    print(f"   Contrasena: admin123")
print("\n Ahora puedes ejecutar: python manage.py runserver")