from django.shortcuts import render
import requests

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


