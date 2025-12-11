from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactoForm
from django.contrib import messages

def contacto(request):
    """
    Vista para mostrar y procesar el formulario de contacto.
    """
    if request.method == 'POST':
        # 1. Crear instancia del formulario con los datos POST
        form = ContactoForm(request.POST)
        
        # 2. Validar los datos
        if form.is_valid():
            # Obtener datos limpios
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            
            # 3. Construir el contenido del correo
            contenido_email = f"Mensaje de {nombre} ({email}):\n\n{mensaje}"
            
            # 4. Enviar el correo
            try:
                send_mail(
                    subject=asunto,
                    message=contenido_email,
                    from_email=settings.DEFAULT_FROM_EMAIL, 
                    recipient_list=['pobarinfo25@gmail.com'], 
                    fail_silently=False,
                )
                messages.success(request, "Tu mensaje ha sido enviado con éxito.")
                
                # pagina de exito despues de enviar el correo
                return redirect('apps.contacto:contacto_gracias') 
            
            except Exception as e:
                messages.error(request, f"Ocurrió un error al enviar el mensaje: {e}")
                pass
    
    else:
        
        form = ContactoForm()
        
    
    return render(request, 'contacto/contacto_form.html', {'form': form})

def contacto_gracias(request):
    """
    Vista simple para mostrar un mensaje de agradecimiento.
    """
    return render(request, 'contacto/contacto_gracias.html')
