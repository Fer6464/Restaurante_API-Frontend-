from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
import requests
from .pedido import PedidoBorrador

@login_required
@permission_required('sistema_restaurante.puede_ver_tablero', raise_exception=True)
def categorias(request):
    try:
        response = requests.get('https://api-restaurante.fastapicloud.dev/menu/categorias/', timeout=5)
        response.raise_for_status()
        categorias = response.json()
    except Exception:
        categorias = []

    return render(request, 'sistema_restaurante/categorias.html', {'categorias': categorias})

@login_required
@permission_required('sistema_restaurante.puede_ver_tablero', raise_exception=True)
def platos_categoria(request, id):
    try:
        response = requests.get(f'https://api-restaurante.fastapicloud.dev/menu/{id}/items/', timeout=5)
        response.raise_for_status()
        platos_categoria = response.json()
    except Exception:
        platos_categoria = []

    return render(request, 'sistema_restaurante/platos_categoria.html', {'platos_categoria': platos_categoria})

@login_required
@permission_required('sistema_restaurante.puede_ver_tablero', raise_exception=True)
def comandas_activas(request):
    try:
        response = requests.get('https://api-restaurante.fastapicloud.dev/pedidos/activos/', timeout=5)
        response.raise_for_status()
        comandas = response.json()
    except Exception:
        comandas = []

    return render(request, 'sistema_restaurante/comandas.html', {'comandas': comandas})

@login_required
@permission_required('sistema_restaurante.puede_ver_tablero', raise_exception=True)
def comanda_detalle(request, pedido_id):
    try:
        response = requests.get('https://api-restaurante.fastapicloud.dev/pedidos/activos/', timeout=5)
        response.raise_for_status()
        comandas_activas = response.json()
        detalle_comanda = next((p for p in comandas_activas if p.get('id') == pedido_id), {})
    except Exception:
        detalle_comanda = {}

    return render(request, 'sistema_restaurante/comanda_detalle.html', {'pedido': detalle_comanda})

@login_required
@permission_required('sistema_restaurante.puede_crear_comandas', raise_exception=True)
def crear_comanda(request):
    return render(request, 'sistema_restaurante/crear_comanda.html', {})


@login_required
@permission_required('sistema_restaurante.puede_crear_comandas', raise_exception=True)
def agregar_platos_comanda(request):
    if request.method == 'POST':
        pedido = PedidoBorrador(request)
        platos_agregados = 0

        # Iteramos sobre los datos enviados en el POST
        for key, value in request.POST.items():
            # Buscamos los inputs con el formato: "plato_<id>"
            if key.startswith('plato_'):
                try:
                    item_menu_id = int(key.split('_')[1])
                    cantidad = int(value)
                    
                    # Solo agregamos si el usuario seleccionó 1 o más
                    if cantidad > 0:
                        pedido.agregar_detalle(item_menu_id=item_menu_id, cantidad=cantidad)
                        platos_agregados += cantidad
                except (ValueError, IndexError):
                    continue
        
        if platos_agregados > 0:
            messages.success(request, f"Se agregaron {platos_agregados} platos a la comanda.")
        else:
            messages.warning(request, "No seleccionaste ninguna cantidad para agregar.")

        # Puedes redirigir a la misma categoría o directamente a la pantalla de crear comanda
        return redirect(request.META.get('HTTP_REFERER', 'sistema_restaurante:categorias'))
    
    return redirect('sistema_restaurante:categorias')