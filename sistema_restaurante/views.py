from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
import requests

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