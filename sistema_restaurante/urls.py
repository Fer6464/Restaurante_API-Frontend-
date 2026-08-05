from django.urls import path
from . import views

app_name = 'sistema_restaurante'

urlpatterns = [
    path('sistema/categorias', views.categorias, name='categorias'),
    path('sistema/categorias/<int:id>/platos', views.platos_categoria, name='platos_categoria'),
]
