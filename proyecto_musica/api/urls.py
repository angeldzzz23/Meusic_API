from django.urls import path
from .views import UsuariosView
from .views import GeneroView
from .views import UsaurioArtistaView
from .views import HabilidadView
from .views import UsuarioHabiliadView
from .views import GeneroMusicalView
from .views import UsuarioGeneroMusicalView
urlpatterns = [
    path('usuarios/', UsuariosView.as_view(), name='usuarios_lista'),
    path('usuarios/<int:id>', UsuariosView.as_view(), name='usuario_por_id'),
    path('genero/', GeneroView.as_view(), name='generos_lista'),
    path('genero/<str:name>', GeneroView.as_view(), name='generos_nombre'),
    path('genero_musical/<str:name>', GeneroMusicalView.as_view(), name='generos_musical_nombre'),
    path('genero_musical/', GeneroMusicalView.as_view(), name='generos_musical_nombre'),
    path('usuarios/artistas/<int:id>', UsaurioArtistaView.as_view(), name='generos_nombre'),
    path('usuarios/artistas/', UsaurioArtistaView.as_view(), name='generos_nombre'),
    path('habilidad/<str:name>', HabilidadView.as_view(), name='habilidad'),
    path('habilidad/', HabilidadView.as_view(), name='habilidad'),
    path('usuarios/habilidad/<int:id>', UsuarioHabiliadView.as_view(), name='usuario_habilidad'),
    path('usuarios/habilidad/', UsuarioHabiliadView.as_view(), name='usuario_habilidad'),
    path('usuarios/genero_musical/<int:id>', UsuarioGeneroMusicalView.as_view(), name='usuario_habilidad'),
    path('usuarios/genero_musical/', UsuarioGeneroMusicalView.as_view(), name='usuario_habilidad'),
]
