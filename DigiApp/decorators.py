from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect


def es_administrador(user):
    return user.is_authenticated and user.groups.filter(name='Administradores').exists()

def es_directivo(user):
    return user.is_authenticated and user.groups.filter(name='Directivos').exists()

def es_operativo(user):
    return user.is_authenticated and user.groups.filter(name='Operativos').exists()


def admin_required(view_func):
    

    def wrapper(request, *args, **kwargs):
        if es_administrador(request.user):
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'No tienes permiso para acceder a esa página.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
    return wrapper


def login_required_directivo_or_admin(view_func):

    def wrapper(request, *args, **kwargs):
        if es_directivo(request.user) or es_administrador(request.user):
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'No tienes permiso para acceder a esa página.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
    return wrapper
