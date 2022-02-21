from django.urls import path
from .views import UsuariosView

urlpatterns = [
    path('usuarios/', UsuariosView.as_view(), name='usuarios_list'),
    path('usuarios/<int:id>', UsuariosView.as_view(), name='usuario_por_id')
    
]
