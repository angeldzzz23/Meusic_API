from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Usuarios
from .models import Genero
from .models import usuario_artista
import json

# Create your views here.


class UsuariosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            datos_usuarios = list(Usuarios.objects.select_related('Genero').filter(usuario_id=id).values())
            if len(datos_usuarios) > 0:
                informacion = datos_usuarios[0]
                datos = {'codigo':"200",'message': "Success", 'usuarios': informacion}
            else:
                datos = {'codigo':"200",'message': "Users not found..."}
            return JsonResponse(datos)
        else:
            datos_usuarios = list(Usuarios.objects.values())
            if len(datos_usuarios) > 0:
                datos = {'codigo':"200", 'message': "Success", 'usuarios': datos_usuarios}
            else:
                datos = {'codigo':"400",'message': "Users not found..."}
            return JsonResponse(datos)

    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
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
            username=jd['username'],contrasena=jd['contrasena'],acerca_de_mi=jd['acerca_de_mi'],
            genero_id=jd['genero_id']
            )
            datos = {'codigo':"200",'message': "Success"}
       
            return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        registro= Usuarios.objects.filter(username=jd['username'])
        if len(registro) > 0:
            datos = {'codigo':"400",'message': "El username ya existe"}  
            return JsonResponse(datos)
        registro= Usuarios.objects.filter(correo_electronico=jd['correo_electronico'])
        if len(registro) > 0:
            datos = {'codigo':"400",'message': "El correo electronico ya existe"}   
            return JsonResponse(datos)
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
            datos = {'codigo':"200",'message': "Success"}
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
                datos = {'codigo':"200",'message': "Success", 'usuarios': informacion}
            return JsonResponse(datos)
        else:
            datos_generos = list(Genero.objects.values())
            if len(datos_generos) > 0:
                datos = {'codigo':"200", 'message': "Success", 'Generos': datos_generos}
            else:
                datos = {'codigo':"400",'message': "Genero not found..."}
            return JsonResponse(datos)

class UsaurioArtistaIdView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id!=0):
            artistas = list(usuario_artista.objects.filter(usuario_id=id).values())
            if len(artistas) > 0:
                informacion = artistas
                datos = {'codigo':"200",'message': "Success", 'artistas': informacion}
            else:
                datos = {'codigo':"400",'message': "artistas not found..."}
            return JsonResponse(datos)