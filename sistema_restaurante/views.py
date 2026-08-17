# views.py
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

        for key, value in request.POST.items():
            if key.startswith('plato_'):
                try:
                    item_menu_id = int(key.split('_')[1])
                    cantidad = int(value)
                    nombre_plato = request.POST.get(f'nombre_{item_menu_id}', '')
                    
                    if cantidad > 0:
                        pedido.agregar_detalle(
                            item_menu_id=item_menu_id, 
                            cantidad=cantidad, 
                            nombre=nombre_plato
                        )
                        platos_agregados += cantidad
                except (ValueError, IndexError):
                    continue
        
        if platos_agregados > 0:
            messages.success(request, f"Se agregaron {platos_agregados} platos a la comanda.")
        else:
            messages.warning(request, "No seleccionaste ninguna cantidad para agregar.")

        return redirect('sistema_restaurante:categorias')
    
    return redirect('sistema_restaurante:categorias')

@login_required
@permission_required('sistema_restaurante.puede_crear_comandas', raise_exception=True)
def ver_borrador(request):
    """
    Renderiza la plantilla del borrador de la comanda.
    Si faltan nombres en la sesión, consulta la API para autocompletarlos.
    """
    pedido = PedidoBorrador(request)
    detalles = pedido.pedido.get('detalles', [])
    
    # Si algún elemento no tiene nombre guardado, consultamos el menú para mapearlos
    if any(not d.get('nombre') for d in detalles):
        try:
            response = requests.get('https://api-restaurante.fastapicloud.dev/menu/', timeout=5)
            if response.status_code == 200:
                menu_items = response.json()
                mapa_nombres = {item['id']: item['nombre'] for item in menu_items if 'id' in item and 'nombre' in item}
                for d in detalles:
                    if not d.get('nombre') and d.get('item_menu_id') in mapa_nombres:
                        d['nombre'] = mapa_nombres[d['item_menu_id']]
                pedido.guardar()
        except Exception:
            pass

    return render(request, 'sistema_restaurante/borrador_comanda.html', {})

@login_required
@permission_required('sistema_restaurante.puede_crear_comandas', raise_exception=True)
def agregar_comanda(request):
    if request.method == 'POST':
        pedido = PedidoBorrador(request)

        numero_mesa = request.POST.get('numero_mesa', '').strip()
        nombre_referencia = request.POST.get('nombre_referencia', '').strip()

        if not numero_mesa or not nombre_referencia:
            messages.error(request, "Debes ingresar el número de mesa y el nombre de referencia.")
            return redirect('sistema_restaurante:ver_borrador')

        pedido.actualizar_cabecera(
            mesa=numero_mesa,
            nombre_ref=nombre_referencia
        )

        detalles = pedido.pedido.get('detalles', [])
        if not detalles:
            messages.error(request, "No hay platos agregados en el borrador para realizar la comanda.")
            return redirect('sistema_restaurante:ver_borrador')

        # Payload mapeado exactamente a los tipos requeridos por FastAPI
        payload = {
            "emisor_id": int(pedido.pedido.get("emisor_id", 1)),
            "grupo_id": int(pedido.pedido.get("grupo_id", 1)),
            "prioridad": str(pedido.pedido.get("prioridad", "normal")),
            "origen_pedido": str(pedido.pedido.get("origen_pedido", "web")),
            "numero_mesa": str(numero_mesa),  # Debe ser STRING según la especificación
            "nombre_referencia": str(nombre_referencia),
            "detalles": [
                {
                    "item_menu_id": int(d["item_menu_id"]),
                    "cantidad": int(d["cantidad"]),
                    "notas": str(d.get("notas", "") or "")
                }
                for d in detalles
            ]
        }

        try:
            response = requests.post(
                'https://api-restaurante.fastapicloud.dev/pedidos/',
                json=payload,
                timeout=5
            )
            response.raise_for_status()

            pedido.limpiar()
            messages.success(request, "¡Comanda realizada con éxito y enviada a cocina!")
            return redirect('sistema_restaurante:comandas_activas')

        except requests.RequestException as e:
            detalle_error = ""
            if hasattr(e, 'response') and e.response is not None:
                try:
                    datos_error = e.response.json()
                    detalle_error = f": {datos_error.get('detail', datos_error)}"
                except Exception:
                    detalle_error = f": {e.response.text}"

            messages.error(request, f"Error de validación en la API{detalle_error}")
            return redirect('sistema_restaurante:ver_borrador')

    return redirect('sistema_restaurante:ver_borrador')

@login_required
@permission_required('sistema_restaurante.puede_crear_comandas', raise_exception=True)
def cancelar_comanda(request):
    pedido = PedidoBorrador(request)
    pedido.limpiar()
    messages.info(request, "La comanda ha sido cancelada.")
    return redirect('sistema_restaurante:categorias')