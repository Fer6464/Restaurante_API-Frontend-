from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests

@login_required
def categorias(request):
    try:
        response = requests.get('https://api-restaurante.fastapicloud.dev/menu/categorias/', timeout=5)
        response.raise_for_status()
        categorias = response.json()
    except Exception:
        categorias = []

    return render(request, 'sistema_restaurante/categorias.html', {'categorias': categorias})

@login_required
def platos_categoria(request, id):
    try:
        response = requests.get(f'https://api-restaurante.fastapicloud.dev/menu/{id}/items/', timeout=5)
        response.raise_for_status()
        platos_categoria = response.json()
    except Exception:
        platos_categoria = []

    return render(request, 'sistema_restaurante/platos_categoria.html', {'platos_categoria': platos_categoria})


@login_required
def comandas_activas(request):
    try:
        response = requests.get('https://api-restaurante.fastapicloud.dev/pedidos/activos/', timeout=5)
        response.raise_for_status()
        comandas = response.json()
    except Exception as e:
        comandas = []

    return render(request, 'sistema_restaurante/comandas.html', {'comandas': comandas})

@login_required
def comanda_detalle(request, pedido_id):
    try:
        response = requests.get('https://api-restaurante.fastapicloud.dev/pedidos/activos/', timeout=5)
        response.raise_for_status()
        comandas_activas = response.json()
        detalle_comanda = next((p for p in comandas_activas if p.get('id') == pedido_id), {})
    except Exception as e:
        detalle_comanda = {}

    return render(request, 'sistema_restaurante/comanda_detalle.html', {'pedido': detalle_comanda})