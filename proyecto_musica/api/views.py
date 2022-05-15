from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Usuarios
from .models import Genero
from .models import Usuario_artista
from .models import Habilidad
from .models import Usuario_habilidad
from .models import Usuario_genero_musical
from .models import Genero_musical
from .models import Usuario_plataforma
from .models import Vimeo
from .models import Youtube
from .models import Spotify
import json
from django.contrib.auth.hashers import make_password
# Create your views here.


class UsuariosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=""):
        print(id)
        if (id !=""):
            datos_usuarios = list(Usuarios.objects.prefetch_related('Genero').filter(usuario_id=id).values(
                "genero__genero_descripcion","genero_id","nombre","apellidos","fecha_nacimiento","username","acerca_de_mi","correo_electronico"))
            if len(datos_usuarios) > 0:
                informacion = datos_usuarios[0]
                
                datos = {'codigo':"200",'message': "Success", 'result': informacion}
            else:
                datos = {'codigo':"200",'message': "Users not found..."}
            return JsonResponse(datos)
        else:
            datos_usuarios = list(Usuarios.objects.prefetch_related('Genero').values("genero__genero_descripcion","genero_id","nombre","apellidos","fecha_nacimiento","username","acerca_de_mi","correo_electronico"))
            if len(datos_usuarios) > 0:
                datos = {'codigo':"200", 'message': "Success", 'result': datos_usuarios}
            else:
                datos = {'codigo':"400",'message': "Users not found..."}
            return JsonResponse(datos)

    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # 
        registro= Usuarios.objects.filter(username=jd['username'])
        if len(registro) > 0:
            datos = {'codigo':"400",'message': "El username ya existe"}  
            return JsonResponse(datos)
        registro= Usuarios.objects.filter(correo_electronico=jd['correo_electronico'])
        if len(registro) > 0:
            datos = {'codigo':"400",'message': "El correo electronico ya existe"}   
            return JsonResponse(datos)
        if len(registro) == 0:
            Usuarios.objects.create(nombre=jd['nombre'],apellidos=jd['apellidos'],
            correo_electronico=jd['correo_electronico'],fecha_nacimiento=jd['fecha_nacimiento'],
            username=jd['username'],contrasena=make_password(jd['contrasena']),acerca_de_mi=jd['acerca_de_mi'],
            genero_id=jd['genero_id']
            )
            registro = list(Usuarios.objects.filter(correo_electronico=jd['correo_electronico']).values())
            
            datos = {'codigo':"200",'message': "Success","result":registro}
       
            return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        registro= Usuarios.objects.filter(username=jd['username'])
        usuario_edit= list(Usuarios.objects.filter(usuario_id=id).values())
        if len(usuario_edit) > 0:
            registro = Usuarios.objects.get(usuario_id=id)
            registro.nombre=jd['nombre']
            registro.apellidos=jd['apellidos']
            registro.correo_electronico=jd['correo_electronico']
            registro.fecha_nacimiento=jd['fecha_nacimiento']
            registro.username=jd['username']
            registro.contrasena=jd['contrasena']
            registro.acerca_de_mi=jd['acerca_de_mi']
            registro.genero_id=jd['genero_id']
            registro.save()
            registro = list(Usuarios.objects.filter(correo_electronico=jd['correo_electronico']).values(  
            "nombre","apellidos","fecha_nacimiento","username","acerca_de_mi","correo_electronico"))
            datos = {'codigo':"200",'message': "Success","result":registro}
       
        else:
            datos = {'codigo':"400",'message': "User not found..."}
        return JsonResponse(datos)

    def delete(self, request, id):
        registro = list(Usuarios.objects.filter(usuario_id=id).values())
        if len(registro) > 0:
            Usuarios.objects.filter(usuario_id=id).delete()
            datos = {'codigo':"200",'message': "Success"}
        else:
            datos = {'codigo':"400",'message': "User not found..."}
        return JsonResponse(datos)

class GeneroView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, name=0):
        if (name != 0):
            datos_generos = list(Genero.objects.filter(genero_descripcion__icontains=name).values())
            if len(datos_generos) > 0:
                informacion = datos_generos
                datos = {'codigo':"200",'message': "Success", 'result': informacion}
                return JsonResponse(datos)
            else:
                datos = {'codigo':"400",'message': "Genero not found..."} 
                return JsonResponse(datos)
        else:
            datos_generos = list(Genero.objects.values())
            if len(datos_generos) > 0:
                datos = {'codigo':"200", 'message': "Success", 'result': datos_generos}
                return JsonResponse(datos)
            else:
                datos = {'codigo':"400",'message': "Genero not found..."}
                return JsonResponse(datos)

class GeneroMusicalView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, name=0):
        if (name != 0):
            datos_generos = list(Genero_musical.objects.filter(genero_musical_descripcion__icontains=name).values())
            if len(datos_generos) > 0:
                informacion = datos_generos
                datos = {'codigo':"200",'message': "Success", 'result': informacion}
                return JsonResponse(datos)
            else:
                 datos = {'codigo':"400",'message': "Genero Musical not found..."}
                 return JsonResponse(datos)
        else:
            datos_generos = list(Genero_musical.objects.values())
            if len(datos_generos) > 0:
                datos = {'codigo':"200", 'message': "Success", 'result': datos_generos}
            else:
                datos = {'codigo':"400",'message': "Genero not found..."}
            return JsonResponse(datos)
    def post(self, request):
            # print(request.body)
            jd = json.loads(request.body)
            Genero_musical.objects.create(genero_musical_descripcion=jd['genero_musical_descripcion'] )
            datos = {'codigo':"200",'message': "Success"}
            return JsonResponse(datos)

class HabilidadView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, name=""):
        if (name != ""):
            datos_habilidad = list(Habilidad.objects.filter(habilidad_descripcion__icontains=name).values())
            if len(datos_habilidad) > 0:
                informacion = datos_habilidad
                datos = {'codigo':"200",'message': "Success", 'result': informacion}
                return JsonResponse(datos)
        else:
            datos_habilidad = list(Habilidad.objects.values())
            if len(datos_habilidad) > 0:
                datos = {'codigo':"200", 'message': "Success", 'result': datos_habilidad}
            else:
                datos = {'codigo':"400",'message': "Habilidades not found..."}
            return JsonResponse(datos)

class UsaurioArtistaView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=""):
        if (id!=""):
            artistas = list(Usuario_artista.objects.filter(usuario_id=id).values())
            if len(artistas) > 0:
                informacion = artistas
                datos = {'codigo':"200",'message': "Success", 'result': informacion}
            else:
                datos = {'codigo':"400",'message': "artistas not found..."}
            return JsonResponse(datos)
    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
        registro= Usuario_artista.objects.filter(usuario_id=jd['usuario_id'])
        if len(registro) ==5:
            datos = {'codigo':"400",'message': "Solo debe elegir 5 artirtas favoritos"}  
            return JsonResponse(datos)
        registro= Usuario_artista.objects.filter(usuario_id=jd['usuario_id'],artista_id=jd['artista_id'])
        if len(registro) >0:
            datos = {'codigo':"400",'message': "Artista previamente guaradado como favorito"}  
            return JsonResponse(datos)
        if len(registro) <5:
            Usuario_artista.objects.create(usuario_id=jd['usuario_id'],artista_id=jd['artista_id'],
           
            )
            datos = {'codigo':"201",'message': "Success"}
       
            return JsonResponse(datos)
    def delete(self, request, id):
        jd = json.loads(request.body)
        registro = list(usuario_artista.objects.filter(usuario_id=id,artista_id=jd['artista_id']).values())
        if len(registro) > 0:
            usuario_artista.objects.filter(usuario_id=id,artista_id=jd['artista_id']).delete()
            datos = {'codigo':"200",'message': "Success"}
        else:
            datos = {'codigo':"400",'message': "El usuario ya no se encuentra relacionado con el artita"}
        return JsonResponse(datos)


class UsuarioHabiliadView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id!=0):
            habilidad = list(Usuario_habilidad.objects.prefetch_related('Habilidad').filter(usuario_id=id).values(
                "habilidad__habilidad_descripcion","habilidad__habilidad_id"
            ))
            if len(habilidad) > 0:
                informacion = habilidad
                datos = {'codigo':"200",'message': "Success", 'artistas': informacion}
                return JsonResponse(datos)
            else:
                datos = {'codigo':"400",'message': "artistas not found..."}
                return JsonResponse(datos)
    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
        registro= Usuario_habilidad.objects.filter(usuario_id=jd['usuario_id'])
        if len(registro) ==5:
            datos = {'codigo':"400",'message': "Solo debe elegir 5 habilidades"}  
            return JsonResponse(datos)
        registro= Usuario_habilidad.objects.filter(usuario_id=jd['usuario_id'],habilidad_id=jd['habilidad_id'])
        if len(registro) >0:
            datos = {'codigo':"400",'message': "Habilidad previamente guaradada"}  
            return JsonResponse(datos)
        if len(registro) <5:
            Usuario_habilidad.objects.create(usuario_id=jd['usuario_id'],habilidad_id=jd['habilidad_id'],
           
            )
            datos = {'codigo':"201",'message': "Success"}
       
        return JsonResponse(datos)
    def delete(self, request, id):
        jd = json.loads(request.body)
        registro = list(Usuario_habilidad.objects.filter(usuario_id=id,habilidad_id=jd['habilidad_id']).values())
        if len(registro) > 0:
            Usuario_habilidad.objects.filter(usuario_id=id,habilidad_id=jd['habilidad_id']).delete()
            datos = {'codigo':"200",'message': "Success"}
        else:
            datos = {'codigo':"400",'message': "El usuario ya no se encuentra relacionado con el artita"}
        return JsonResponse(datos)

class UsuarioGeneroMusicalView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id!=0):
            genero = list(Usuario_genero_musical.objects.prefetch_related('genero_musical').filter(usuario_id=id).values(
                "genero_musical__genero_musical_descripcion","genero_musical__genero_musical_id"
            ))
            if len(genero) > 0:
                informacion = genero
                datos = {'codigo':"200",'message': "Success", 'generos_musicales': informacion}
            else:
                datos = {'codigo':"400",'message': "generos musicales not found..."}
            return JsonResponse(datos)
    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
        registro= Usuario_genero_musical.objects.filter(usuario_id=jd['usuario_id'])
        if len(registro) ==5:
            datos = {'codigo':"400",'message': "Solo debe elegir 5 generos de musica"}  
            return JsonResponse(datos)
        registro= Usuario_genero_musical.objects.filter(usuario_id=jd['usuario_id'],genero_musical_id=jd['genero_musical_id'])
        if len(registro) >0:
            datos = {'codigo':"400",'message': "Genero musical previamente guaradado"}  
            return JsonResponse(datos)
        if len(registro) <5:
            Usuario_genero_musical.objects.create(usuario_id=jd['usuario_id'],genero_musical_id=jd['genero_musical_id'],
           
            )
            datos = {'codigo':"201",'message': "Success"}
       
            return JsonResponse(datos)
    def delete(self, request, id):
        jd = json.loads(request.body)
        registro = list(Usuario_genero_musical.objects.filter(usuario_id=id,genero_musical_id=jd['genero_musical_id']).values())
        if len(registro) > 0:
            Usuario_genero_musical.objects.filter(usuario_id=id,genero_musical_id=jd['genero_musical_id']).delete()
            datos = {'codigo':"200",'message': "Success"}
        else:
            datos = {'codigo':"400",'message': "El usuario ya no se encuentra relacionado con el artita"}
        return JsonResponse(datos)

class UsuarioPlataformaView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=""):
        if (id!=""):
            genero = list(Usuario_plataforma.objects.filter(usuario_id=id).values())
            if len(genero) > 0:
                informacion = genero
                datos = {'codigo':"200",'message': "Success", 'result': informacion}
            else:
                datos = {'codigo':"400",'message': "Usuario Plataforma not found..."}
            return JsonResponse(datos)
    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
       
        Usuario_plataforma.objects.create(usuario_id=jd['usuario_id'],plataforma_id=jd['plataforma_id'],
        url=jd['url'] )
        datos = {'codigo':"201",'message': "Success"}
        return JsonResponse(datos)

    def delete(self, request, id):
        jd = json.loads(request.body)
        registro = list(Usuario_plataforma.objects.filter(usuario_id=id,plataforma_id=jd['plataforma_id']).values())
        if len(registro) > 0:
            Usuario_plataforma.objects.filter(usuario_id=id,plataforma_id=jd['plataforma_id']).delete()
            datos = {'codigo':"200",'message': "Success"}
        else:
            datos = {'codigo':"400",'message': "Registro previamente Borrado"}
        return JsonResponse(datos)

class VimeoView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, name=0):
        vimeo = list(Vimeo.objects.filter(vimeo_id=1).values())
        informacion = vimeo
        datos = {'codigo':"200",'message': "Success", 'result': informacion}
        return JsonResponse(datos)
class YoutubeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, name=0):
        youtube = list(Youtube.objects.filter(youtube_id=1).values())
        informacion = youtube
        datos = {'codigo':"200",'message': "Success", 'result': informacion}
        return JsonResponse(datos)

class SpotifyView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, name=0):
        spotify = list(Spotify.objects.filter(spotify_id=1).values())
        informacion = spotify
        datos = {'codigo':"200",'message': "Success", 'result': informacion}
        return JsonResponse(datos)

       

