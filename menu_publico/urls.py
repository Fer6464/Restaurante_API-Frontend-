from django.urls import path
from . import views

app_name = 'menu_publico'

urlpatterns = [
    path('', views.index, name='menu_index'),
]


