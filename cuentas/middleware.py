from datetime import datetime
from django.utils.timezone import now

class UltimaActividadMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            perfil = getattr(request.user, 'userprofile', None)
            if perfil:
                perfil.ultima_actividad = now()
                perfil.save(update_fields=['ultima_actividad'])
        return self.get_response(request)
