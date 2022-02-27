from django.urls import path
from .views import UsuariosView
from .views import GeneroView
from .views import UsaurioArtistaIdView
urlpatterns = [
    path('usuarios/', UsuariosView.as_view(), name='usuarios_lista'),
    path('usuarios/<int:id>', UsuariosView.as_view(), name='usuario_por_id'),
    path('genero/', GeneroView.as_view(), name='generos_lista'),
    path('genero/<str:name>', GeneroView.as_view(), name='generos_nombre'),
    path('usuarios/artistas/<int:id>', UsaurioArtistaIdView.as_view(), name='generos_nombre')
    
]
