from django.urls import path
from . import views

app_name = 'sistema_restaurante'

urlpatterns = [
    path('sistema/categorias', views.categorias, name='categorias'),
    path('sistema/categorias/<int:id>/platos', views.platos_categoria, name='platos_categoria'),
    path('sistema/comandas/', views.comandas_activas, name='comandas_activas'),
    path('sistema/comandas/<int:pedido_id>/', views.comanda_detalle, name='comanda_detalle'),
]


