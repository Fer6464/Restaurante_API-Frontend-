from django.shortcuts import render
import requests
from .pedido import PedidoBorrador

def index(request):
    try:
        response = requests.get('https://api-restaurante.fastapicloud.dev/menu/', timeout=5)
        response.raise_for_status()
        platos = response.json()
        if isinstance(platos, list):
            platos = sorted(platos, key=lambda item: item.get('categoria', 'Otros'))
    except Exception as e:
        platos = []
    
    return render(request, 'menu_publico/index.html', {'platos': platos})

def categorias(request):
    try:
        response = requests.get('https://api-restaurante.fastapicloud.dev/menu/categorias/', timeout=5)
        response.raise_for_status()
        categorias = response.json()
        
    except Exception as e:
            categorias = []

    return render(request, 'sistema_restaurante/categorias.html', {'categorias': categorias})

def platos_categoria(request, id):
    try:
        response = requests.get(f'https://api-restaurante.fastapicloud.dev/menu/{id}/items/', timeout=5)
        response.raise_for_status()
        platos_categoria = response.json()
        
    except Exception as e:
            platos_categoria = []

    return render(request, 'sistema_restaurante/platos_categoria.html', {'platos_categoria': platos_categoria})