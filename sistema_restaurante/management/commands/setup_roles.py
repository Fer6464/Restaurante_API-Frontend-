from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Configura los grupos y asigna los permisos para Equipo de Cocina y Meseros/Barra'

    def handle(self, *args, **kwargs):
        try:
            perm_ver_tablero = Permission.objects.get(codename='puede_ver_tablero')
            perm_crear_comandas = Permission.objects.get(codename='puede_crear_comandas')
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Error: Los permisos personalizados no existen en la base de datos. Por favor ejecuta "python manage.py migrate" primero.'
            ))
            return

        # 1. Crear grupo Equipo de Cocina y asignar solo el permiso de ver tablero
        grupo_cocina, created_cocina = Group.objects.get_or_create(name='Equipo de Cocina')
        grupo_cocina.permissions.set([perm_ver_tablero])
        if created_cocina:
            self.stdout.write(self.style.SUCCESS('Grupo "Equipo de Cocina" creado con éxito.'))
        else:
            self.stdout.write(self.style.SUCCESS('Grupo "Equipo de Cocina" actualizado con éxito.'))

        # 2. Crear grupo Meseros y Barra y asignar ambos permisos
        grupo_meseros, created_meseros = Group.objects.get_or_create(name='Meseros y Barra')
        grupo_meseros.permissions.set([perm_ver_tablero, perm_crear_comandas])
        if created_meseros:
            self.stdout.write(self.style.SUCCESS('Grupo "Meseros y Barra" creado con éxito.'))
        else:
            self.stdout.write(self.style.SUCCESS('Grupo "Meseros y Barra" actualizado con éxito.'))

        self.stdout.write(self.style.SUCCESS('¡Configuración de roles completada exitosamente!'))
