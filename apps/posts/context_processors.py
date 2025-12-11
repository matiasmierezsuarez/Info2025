from datetime import date
from .models import Banner

def banners_globales(request):
    """
    Context processor para hacer los banners disponibles en todos los templates
    """
    hoy = date.today()
    
    # Filtrar banners activos
    banners_activos = Banner.objects.filter(activo=True)
    
    # Filtrar por fechas si están definidas
    banners_vigentes = []
    for banner in banners_activos:
        if banner.fecha_inicio and banner.fecha_inicio > hoy:
            continue
        if banner.fecha_fin and banner.fecha_fin < hoy:
            continue
        banners_vigentes.append(banner)
    
    # Organizar banners por posición (ordenados por 'orden')
    return {
        'banners_principales': sorted([b for b in banners_vigentes if b.posicion == 'principal'], key=lambda x: x.orden)[:5],
        'banners_laterales': sorted([b for b in banners_vigentes if b.posicion == 'lateral'], key=lambda x: x.orden)[:5],
        'banners_footer': sorted([b for b in banners_vigentes if b.posicion == 'footer'], key=lambda x: x.orden)[:2],
    }