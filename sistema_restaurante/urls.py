from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'sistema_restaurante'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='sistema_restaurante:categorias', permanent=False)),
    path('sistema/categorias', views.categorias, name='categorias'),
    path('sistema/categorias/<int:id>/platos', views.platos_categoria, name='platos_categoria'),
    path('sistema/comandas/', views.comandas_activas, name='comandas_activas'),
    path('sistema/comandas/nueva/', views.crear_comanda, name='crear_comanda'),
    path('sistema/comandas/<int:pedido_id>/', views.comanda_detalle, name='comanda_detalle'),
]




