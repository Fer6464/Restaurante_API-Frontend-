from django.db import models

class PermisosRestaurante(models.Model):
    class Meta:
        managed = False  # No crea tabla en SQLite
        default_permissions = ()
        permissions = [
            ('puede_ver_tablero', 'Puede ver el tablero de comandas y categorias'),
            ('puede_crear_comandas', 'Puede iniciar el flujo de crear una comanda'),
        ]

