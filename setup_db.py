import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'burger_project.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario
from menu.models import Categoria, Producto

def run():
    print("Iniciando configuración de base de datos...")

    # 1. Crear / Actualizar usuario javiervega
    username = 'javiervega'
    email = 'juandiegosalgado2003@gmail.com'
    password = 'Burger2025!#'

    user, created = User.objects.get_or_create(username=username)
    user.email = email
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    
    if created:
        print(f"Usuario {username} creado exitosamente.")
    else:
        print(f"Usuario {username} actualizado exitosamente.")

    # Asegurar que el perfil existe y no está bloqueado
    perfil, p_created = PerfilUsuario.objects.get_or_create(usuario=user)
    perfil.intentos_fallidos = 0
    perfil.bloqueado = False
    perfil.save()
    print("Perfil de usuario verificado/desbloqueado.")

    # 2. Crear Categorías
    cat_hamburguesas, _ = Categoria.objects.get_or_create(nombre='Hamburguesas', defaults={'icono': '🍔', 'orden': 1})
    cat_bebidas, _ = Categoria.objects.get_or_create(nombre='Bebidas', defaults={'icono': '🥤', 'orden': 2})
    cat_papas, _ = Categoria.objects.get_or_create(nombre='Papas', defaults={'icono': '🍟', 'orden': 3})
    cat_combos, _ = Categoria.objects.get_or_create(nombre='Combos', defaults={'icono': '🥡', 'orden': 4})
    print("Categorías creadas.")

    # 3. Crear Productos
    productos = [
        # Hamburguesas (8)
        {"nombre": "Brutus Clásica", "precio": 15000, "cat": cat_hamburguesas, "desc": "Carne de res 150g, queso cheddar, lechuga, tomate y salsa de la casa.", "destacado": True},
        {"nombre": "Brutus Bacon", "precio": 18000, "cat": cat_hamburguesas, "desc": "Carne de res 150g, doble tocineta crujiente, queso cheddar y salsa BBQ.", "destacado": True},
        {"nombre": "Brutus Doble", "precio": 22000, "cat": cat_hamburguesas, "desc": "Doble carne de res 150g, doble queso, tocineta y vegetales.", "destacado": False},
        {"nombre": "Chicken Brutus", "precio": 16000, "cat": cat_hamburguesas, "desc": "Pechuga de pollo apanada, queso mozzarella, lechuga y mayonesa.", "destacado": False},
        {"nombre": "Brutus Monster", "precio": 25000, "cat": cat_hamburguesas, "desc": "Tres carnes de res, aros de cebolla, tocineta, queso cheddar y salsa especial.", "destacado": True},
        {"nombre": "Brutus Veggie", "precio": 17000, "cat": cat_hamburguesas, "desc": "Hamburguesa de lentejas, queso mozzarella, vegetales frescos y salsa verde.", "destacado": False},
        {"nombre": "Brutus Ranchera", "precio": 19000, "cat": cat_hamburguesas, "desc": "Carne de res, salchicha ranchera, huevo frito, queso y papas ripio.", "destacado": False},
        {"nombre": "Brutus Blue", "precio": 20000, "cat": cat_hamburguesas, "desc": "Carne de res, queso azul, cebolla caramelizada y rúcula.", "destacado": False},

        # Bebidas (4)
        {"nombre": "Coca Cola 400ml", "precio": 4000, "cat": cat_bebidas, "desc": "Gaseosa Coca Cola personal.", "destacado": False},
        {"nombre": "Postobón Manzana 400ml", "precio": 3500, "cat": cat_bebidas, "desc": "Gaseosa Postobón sabor a manzana.", "destacado": False},
        {"nombre": "Colombiana 400ml", "precio": 3500, "cat": cat_bebidas, "desc": "Gaseosa Colombiana la nuestra.", "destacado": False},
        {"nombre": "Jugo Hit Mora 500ml", "precio": 4000, "cat": cat_bebidas, "desc": "Jugo Hit sabor a mora.", "destacado": False},

        # Papas (4)
        {"nombre": "Papas Francesas", "precio": 6000, "cat": cat_papas, "desc": "Porción de papas a la francesa crujientes.", "destacado": False},
        {"nombre": "Papas Rústicas", "precio": 7000, "cat": cat_papas, "desc": "Papas en casco con finas hierbas.", "destacado": False},
        {"nombre": "Papas con Queso y Tocineta", "precio": 10000, "cat": cat_papas, "desc": "Papas a la francesa bañadas en queso cheddar y trozos de tocineta.", "destacado": True},
        {"nombre": "Salchipapas Clásicas", "precio": 12000, "cat": cat_papas, "desc": "Papas francesas con rodajas de salchicha y salsas al gusto.", "destacado": False},

        # Combos (4)
        {"nombre": "Combo Clásico", "precio": 22000, "cat": cat_combos, "desc": "Hamburguesa Brutus Clásica + Papas Francesas + Gaseosa 400ml.", "destacado": True},
        {"nombre": "Combo Bacon", "precio": 25000, "cat": cat_combos, "desc": "Hamburguesa Brutus Bacon + Papas Francesas + Gaseosa 400ml.", "destacado": False},
        {"nombre": "Combo Pareja", "precio": 45000, "cat": cat_combos, "desc": "2 Hamburguesas Clásicas + 2 Papas Francesas + 2 Gaseosas 400ml.", "destacado": True},
        {"nombre": "Combo Familiar", "precio": 85000, "cat": cat_combos, "desc": "4 Hamburguesas Clásicas + 4 Papas Francesas + Gaseosa 1.5L.", "destacado": False},
    ]

    for p in productos:
        prod, p_created = Producto.objects.get_or_create(
            nombre=p["nombre"],
            defaults={
                'precio': p["precio"],
                'categoria': p["cat"],
                'descripcion': p["desc"],
                'destacado': p["destacado"],
                'disponible': True
            }
        )
        if not p_created:
            # Actualizar si ya existe
            prod.precio = p["precio"]
            prod.categoria = p["cat"]
            prod.descripcion = p["desc"]
            prod.destacado = p["destacado"]
            prod.save()

    print("20 productos creados/actualizados con éxito.")

if __name__ == '__main__':
    run()
