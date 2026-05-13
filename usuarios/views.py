from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from .models import PerfilUsuario

MAX_INTENTOS = 5
BLOQUEO_MINUTOS = 15

def login_view(request):
    if request.user.is_authenticated:
        return redirect('panel_personal')

    intentos_usados = 0

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        try:
            user_obj = User.objects.get(username=username)
            perfil, _ = PerfilUsuario.objects.get_or_create(usuario=user_obj)

            if perfil.bloqueado:
                if perfil.bloqueado_hasta and timezone.now() < perfil.bloqueado_hasta:
                    mins = int((perfil.bloqueado_hasta - timezone.now()).total_seconds() / 60) + 1
                    messages.error(request, f'Cuenta bloqueada. Intenta en {mins} minuto(s).')
                    return render(request, 'usuarios/login.html', {'intentos_usados': 5})
                else:
                    perfil.bloqueado = False
                    perfil.intentos_fallidos = 0
                    perfil.save()

            user_auth = authenticate(request, username=username, password=password)

            if user_auth:
                perfil.intentos_fallidos = 0
                perfil.bloqueado = False
                perfil.save()
                
                # CRÍTICO: especificar el backend para que login() funcione
                user_auth.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user_auth)
                messages.success(request, f'¡Bienvenido, {user_auth.first_name or user_auth.username}!')
                return redirect('panel_personal')
            else:
                perfil.intentos_fallidos += 1
                intentos_usados = perfil.intentos_fallidos
                if perfil.intentos_fallidos >= MAX_INTENTOS:
                    perfil.bloqueado = True
                    perfil.bloqueado_hasta = timezone.now() + timedelta(minutes=BLOQUEO_MINUTOS)
                    perfil.save()
                    messages.error(request, f'Cuenta bloqueada por {BLOQUEO_MINUTOS} minutos.')
                    return render(request, 'usuarios/login.html', {'intentos_usados': 5})
                else:
                    perfil.save()
                    restantes = MAX_INTENTOS - perfil.intentos_fallidos
                    messages.error(request, f'Credenciales incorrectas. Te quedan {restantes} intento(s).')
                    intentos_usados = perfil.intentos_fallidos

        except User.DoesNotExist:
            messages.error(request, 'Credenciales incorrectas.')

    return render(request, 'usuarios/login.html', {'intentos_usados': intentos_usados})

def verificar_2fa(request):
    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('inicio')
