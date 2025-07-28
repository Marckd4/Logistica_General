from django.shortcuts import render

# Create your views here.

from django.utils.timezone import now, timedelta
from cuentas.models import UserProfile

def usuarios_activos(request):
    hace_5_minutos = now() - timedelta(minutes=5)
    activos = UserProfile.objects.filter(ultima_actividad__gte=hace_5_minutos)
    return render(request, 'usuarios_activos.html', {'activos': activos})

