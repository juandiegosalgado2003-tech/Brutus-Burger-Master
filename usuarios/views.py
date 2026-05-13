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
                codigo = perfil.generar_codigo_2fa()
                request.session['pre_2fa_user_id'] = user_auth.id

                # Enviar por correo
                if user_auth.email:
                    partes = user_auth.email.split('@')
                    nombre = partes[0]
                    dominio = partes[1]
                    hint = nombre[:3] + '***@' + dominio
                    request.session['email_hint'] = hint
                    try:
                        send_mail(
                            subject='🔐 Tu código de verificación — BurgerSystem',
                            message=f'Hola {user_auth.first_name or user_auth.username},\n\nTu código de verificación es:\n\n  {codigo}\n\nEste código expira en 5 minutos.\nSi no solicitaste este acceso, ignora este mensaje.\n\n— BurgerSystem',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[user_auth.email],
                            fail_silently=False,
                        )
                    except Exception as e:
                        print(f"Error enviando email: {e}")
                        messages.warning(request, 'No se pudo enviar el correo. Contacta al administrador.')

                return redirect('verificar_2fa')
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
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('login')

    email_hint = request.session.get('email_hint', '')

    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo', '').strip()
        try:
            user = User.objects.get(pk=user_id)
            perfil = PerfilUsuario.objects.get(usuario=user)

            if (perfil.codigo_2fa == codigo_ingresado and
                not perfil.codigo_2fa_usado and
                perfil.codigo_2fa_expira and
                timezone.now() < perfil.codigo_2fa_expira):

                perfil.codigo_2fa_usado = True
                perfil.save()

                # CRÍTICO: especificar el backend para que login() funcione
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                for key in ['pre_2fa_user_id', 'email_hint']:
                    request.session.pop(key, None)

                messages.success(request, f'¡Bienvenido, {user.first_name or user.username}!')
                return redirect('panel_personal')
            else:
                messages.error(request, 'Código incorrecto o expirado.')
        except (User.DoesNotExist, PerfilUsuario.DoesNotExist):
            return redirect('login')

    return render(request, 'usuarios/verificar_2fa.html', {'email_hint': email_hint})


def logout_view(request):
    logout(request)
    return redirect('inicio')
