"""
Ejecutar con: python manage.py shell < crear_usuario.py
Crea el usuario javier vega con contraseña segura y perfil 2FA
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'burger_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario

# Borrar si existe
User.objects.filter(username='javiervega').delete()

user = User.objects.create_superuser(
    username='javiervega',
    email='javier@burgersystem.com',
    password='Burger2025!#',
    first_name='Javier',
    last_name='Vega'
)

PerfilUsuario.objects.get_or_create(usuario=user)
print(f"""
✅ Usuario creado exitosamente:
   Usuario:    javiervega
   Contraseña: Burger2025!#
   Email:      javier@burgersystem.com
""")
