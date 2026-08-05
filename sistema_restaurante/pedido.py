# tu_app/pedido.py

class PedidoBorrador:
    def __init__(self, request):
        self.session = request.session
        pedido = self.session.get('pedido_borrador')
        
        # Si no existe en la sesión, inicializamos la estructura base
        if not pedido:
            pedido = self.session['pedido_borrador'] = {
                "emisor_id": 1,
                "grupo_id": 1,
                "prioridad": "normal",
                "origen_pedido": "web",
                "numero_mesa": "",
                "nombre_referencia": "",
                "detalles": []
            }
        self.pedido = pedido

    def agregar_detalle(self, item_menu_id, cantidad=1, notas=""):
        item_menu_id = int(item_menu_id)
        cantidad = int(cantidad)

        # Buscar si el plato/item ya existe en los detalles
        detalle_existente = next(
            (d for d in self.pedido['detalles'] if d['item_menu_id'] == item_menu_id), 
            None
        )

        if detalle_existente:
            detalle_existente['cantidad'] += cantidad
            if notas:
                detalle_existente['notas'] = notas
        else:
            self.pedido['detalles'].append({
                "item_menu_id": item_menu_id,
                "cantidad": cantidad,
                "notas": notas
            })

        self.guardar()

    def actualizar_cabecera(self, mesa=None, nombre_ref=None, prioridad=None, origen=None):
        if mesa is not None:
            self.pedido['numero_mesa'] = str(mesa)
        if nombre_ref is not None:
            self.pedido['nombre_referencia'] = str(nombre_ref)
        if prioridad is not None:
            self.pedido['prioridad'] = str(prioridad)
        if origen is not None:
            self.pedido['origen_pedido'] = str(origen)
            
        self.guardar()

    def eliminar_detalle(self, item_menu_id):
        item_menu_id = int(item_menu_id)
        self.pedido['detalles'] = [
            d for d in self.pedido['detalles'] if d['item_menu_id'] != item_menu_id
        ]
        self.guardar()

    def guardar(self):
        # Indicar a Django expresamente que la sesión fue modificada
        self.session.modified = True

    def limpiar(self):
        # Borrar el pedido de la sesión al finalizar la compra/envío
        if 'pedido_borrador' in self.session:
            del self.session['pedido_borrador']
            self.guardar()