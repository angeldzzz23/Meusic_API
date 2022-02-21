from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Usuarios
import json

# Create your views here.


class UsuariosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            datos_usuarios = list(Usuarios.objects.filter(usuario_id=id).values())
            if len(datos_usuarios) > 0:
                informacion = datos_usuarios[0]
                datos = {'codigo':"200",'message': "Success", 'usuarios': informacion}
            else:
                datos = {'message': "Users not found..."}
            return JsonResponse(datos)
        else:
            datos_usuarios = list(Usuarios.objects.values())
            if len(datos_usuarios) > 0:
                datos = {'codigo':"200", 'message': "Success", 'usuarios': datos_usuarios}
            else:
                datos = {'message': "Users not found..."}
            return JsonResponse(datos)

    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        # print(jd)
        registro= list(Usuarios.objects.filter(username=jd['username']).values())
        if len(registro) == 0:
            Usuarios.objects.create(nombre=jd['nombre'],apellidos=jd['apellidos'],correo_electronico=jd['correo_electronico'],fecha_nacimiento=jd['fecha_nacimiento'],username=jd['username'],contrasena=jd['contrasena'],acerca_de_mi=jd['acerca_de_mi'])
            datos = {'codigo':"200",'message': "Success"}
        else:
            datos = {'message': "El username ya existe"}  
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
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
            registro.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "User not found..."}
        return JsonResponse(datos)

    def delete(self, request, id):
        registro = list(Usuarios.objects.filter(usuario_id=id).values())
        if len(registro) > 0:
            Usuarios.objects.filter(usuario_id=id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "User not found..."}
        return JsonResponse(datos)