from django.core.exceptions import ObjectDoesNotExist
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
                "genero__genero_descripcion","genero_id","nombre","apellidos",
                "fecha_nacimiento","username","acerca_de_mi","correo_electronico",
                "skill_1_id","skill_2_id","skill_3_id","skill_4_id","skill_5_id"))
            if len(datos_usuarios) > 0:
                informacion = datos_usuarios[0]
                
                datos = {'codigo':"200",'message': "Success", 'result': informacion}
            else:
                datos = {'codigo':"200",'message': "Users not found..."}
            return JsonResponse(datos)
        else:
            datos_usuarios = list(Usuarios.objects.prefetch_related('Genero')
                    .values("genero__genero_descripcion","genero_id","nombre",
                        "apellidos","fecha_nacimiento","username","acerca_de_mi",
                        "correo_electronico","skill_1_id","skill_2_id",
                        "skill_3_id","skill_4_id","skill_5_id"))
            if len(datos_usuarios) > 0:
                datos = {'codigo':"200", 'message': "Success", 'result': datos_usuarios}
            else:
                datos = {'codigo':"400",'message': "Users not found..."}
            return JsonResponse(datos)

    def post(self, request):
        # print(request.body)
        jd = json.loads(request.body)
        
        registro= Usuarios.objects.filter(username=jd['username'])
        if len(registro) > 0:
            datos = {'codigo':"400",'message': "El username ya existe"}  
            return JsonResponse(datos)
        registro= Usuarios.objects.filter(correo_electronico=jd['correo_electronico'])
        if len(registro) > 0:
            datos = {'codigo':"400",'message': "El correo electronico ya existe"}   
            return JsonResponse(datos)
        if len(registro) == 0:

            # error checking
            if 'skill_1' in jd:
                s1 = jd['skill_1']

                if not s1.isnumeric():
                    datos = {'codigo':"400",'message': "Please enter numeric skill id"}
                    return JsonResponse(datos)
                skill_1 = Habilidad.objects.filter(habilidad_id=s1)
                if not skill_1:
                    datos = {'codigo':"400",'message': "Skill not found in database"}
                    return JsonResponse(datos)
                skill_1 = Habilidad.objects.get(habilidad_id=s1)
            else:
                skill_1 = None


            # TODO: for rest of skills
            
            skill_2 = (Habilidad.objects.get(habilidad_id=jd['skill_2']) if 
            'skill_2' in jd else None)
            skill_3 = (Habilidad.objects.get(habilidad_id=jd['skill_3']) if 
            'skill_3' in jd else None)
            skill_4 = (Habilidad.objects.get(habilidad_id=jd['skill_4']) if 
            'skill_4' in jd else None)
            skill_5 = (Habilidad.objects.get(habilidad_id=jd['skill_5']) if 
            'skill_5' in jd else None)
            

            Usuarios.objects.create(nombre=jd['nombre'],apellidos=jd['apellidos'],
            correo_electronico=jd['correo_electronico'],fecha_nacimiento=jd['fecha_nacimiento'],
            username=jd['username'],contrasena=make_password(jd['contrasena']),
            acerca_de_mi=jd['acerca_de_mi'],genero_id=jd['genero_id'],
            skill_1=skill_1,skill_2=skill_2,skill_3=skill_3,skill_4=skill_4,
            skill_5=skill_5
            )

            # post to Usuario_habilidad db
            userid= Usuarios.objects.filter(username=jd['username']).values('usuario_id')

            if 'skill_1' in jd:
                Usuario_habilidad.objects.create(usuario_id=userid,habilidad_id=jd['skill_1'])
            if 'skill_2' in jd:
                Usuario_habilidad.objects.create(usuario_id=userid,habilidad_id=jd['skill_2'])
            if 'skill_3' in jd:
                Usuario_habilidad.objects.create(usuario_id=userid,habilidad_id=jd['skill_3'])
            if 'skill_4' in jd:
                Usuario_habilidad.objects.create(usuario_id=userid,habilidad_id=jd['skill_4'])
            if 'skill_5' in jd:
                Usuario_habilidad.objects.create(usuario_id=userid,habilidad_id=jd['skill_5'])

            registro = list(Usuarios.objects.filter(correo_electronico=jd['correo_electronico']).values())
            
            datos = {'codigo':"200",'message': "Success","result":registro}
       
            return JsonResponse(datos)

    def patch(self, request, id):
        jd = json.loads(request.body)
        registro = Usuarios.objects.filter(username=jd['username'])
        usuario_edit = list(Usuarios.objects.filter(usuario_id=id).values())
        if len(usuario_edit) > 0:
            registro = Usuarios.objects.get(usuario_id=id)
            
            if 'nombre' in jd:
                registro.nombre = jd['nombre']

            if 'apellidos' in jd:
                registro.apellidos = jd['apellidos']

            if 'correo_electronico' in jd:
                registro.correo_electronico = jd['correo_electronico']

            if 'fecha_nacimiento' in jd:
                registro.fecha_nacimiento = jd['fecha_nacimiento']

            if 'username' in jd:
                registro.username = jd['username']

            if 'contrasena' in jd:
                registro.contrasena = jd['contrasena']

            if 'acerca_de_mi' in jd:
                registro.acerca_de_mi = jd['acerca_de_mi']

            if 'genero_id' in jd:
                registro.genero_id = jd['genero_id']

            datos = {'codigo' : "400", 'message' :  "Skill not found in database"}
            if 'skill_1' in jd:
                s1 = jd['skill_1']
                skill_1 = Habilidad.objects.filter(habilidad_id=s1)
                if not skill_1:
                    return JsonResponse(datos)
                skill_1 = Habilidad.objects.get(habilidad_id=s1)
                
                x = Usuario_habilidad.objects.filter(usuario_id=id, habilidad_id=registro.skill_1).values('usuario_habilidad_id').first()
                if not x:
                    Usuario_habilidad.objects.create(usuario_id=id, habilidad_id=jd['skill_1'])
                else:
                    registro_habilidades = Usuario_habilidad.objects.get(usuario_habilidad_id=x['usuario_habilidad_id'])
                    registro_habilidades.usuario_id = id
                    registro_habilidades.habilidad_id = jd['skill_1']
                    registro_habilidades.save()

                registro.skill_1 = skill_1

            if 'skill_2' in jd:
                s2 = jd['skill_2']
                skill_2 = Habilidad.objects.filter(habilidad_id=s2)
                if not skill_2:
                    return JsonResponse(datos)
                skill_2 = Habilidad.objects.get(habilidad_id=s2)
                
                x = Usuario_habilidad.objects.filter(usuario_id=id, habilidad_id=registro.skill_2).values('usuario_habilidad_id').first()
                if not x:
                    Usuario_habilidad.objects.create(usuario_id=id, habilidad_id=jd['skill_2'])
                else:
                    registro_habilidades = Usuario_habilidad.objects.get(usuario_habilidad_id=x['usuario_habilidad_id'])
                    registro_habilidades.usuario_id = id
                    registro_habilidades.habilidad_id = jd['skill_2']
                    registro_habilidades.save()

                registro.skill_2 = skill_2

            if 'skill_3' in jd:
                s3 = jd['skill_3']
                skill_3 = Habilidad.objects.filter(habilidad_id=s3)
                if not skill_3:
                    return JsonResponse(datos)
                skill_3 = Habilidad.objects.get(habilidad_id=s3)
                
                x = Usuario_habilidad.objects.filter(usuario_id=id, habilidad_id=registro.skill_3).values('usuario_habilidad_id').first()
                if not x:
                    Usuario_habilidad.objects.create(usuario_id=id, habilidad_id=jd['skill_3'])
                else:
                    registro_habilidades = Usuario_habilidad.objects.get(usuario_habilidad_id=x['usuario_habilidad_id'])
                    registro_habilidades.usuario_id = id
                    registro_habilidades.habilidad_id = jd['skill_3']
                    registro_habilidades.save()

                registro.skill_3 = skill_3

            if 'skill_4' in jd:
                s4 = jd['skill_4']
                skill_4 = Habilidad.objects.filter(habilidad_id=s4)
                if not skill_4:
                    return JsonResponse(datos)
                skill_4 = Habilidad.objects.get(habilidad_id=s4)
                
                x = Usuario_habilidad.objects.filter(usuario_id=id, habilidad_id=registro.skill_4).values('usuario_habilidad_id').first()
                if not x:
                    Usuario_habilidad.objects.create(usuario_id=id, habilidad_id=jd['skill_4'])
                else:
                    registro_habilidades = Usuario_habilidad.objects.get(usuario_habilidad_id=x['usuario_habilidad_id'])
                    registro_habilidades.usuario_id = id
                    registro_habilidades.habilidad_id = jd['skill_4']
                    registro_habilidades.save()

                registro.skill_4 = skill_4

            if 'skill_5' in jd:
                s5 = jd['skill_5']
                skill_5 = Habilidad.objects.filter(habilidad_id=s5)
                if not skill_5:
                    return JsonResponse(datos)
                skill_5 = Habilidad.objects.get(habilidad_id=s5)
                
                x = Usuario_habilidad.objects.filter(usuario_id=id, habilidad_id=registro.skill_5).values('usuario_habilidad_id').first()
                if not x:
                    Usuario_habilidad.objects.create(usuario_id=id, habilidad_id=jd['skill_5'])
                else:
                    registro_habilidades = Usuario_habilidad.objects.get(usuario_habilidad_id=x['usuario_habilidad_id'])
                    registro_habilidades.usuario_id = id
                    registro_habilidades.habilidad_id = jd['skill_5']
                    registro_habilidades.save()

                registro.skill_5 = skill_5

            registro.save()
            registro = list(Usuarios.objects.filter(correo_electronico=jd['correo_electronico']).values(  
            "nombre","apellidos","fecha_nacimiento","username","acerca_de_mi","correo_electronico",
            "skill_1", "skill_2", "skill_3", "skill_3", "skill_4", "skill_5"))
            datos = {'codigo' : "200", 'message': "Success", "result": registro}
       
        else:
            datos = {'codigo' : "400", 'message' : "User not found..."}
        return JsonResponse(datos)


    def put(self, request, id):
        jd = json.loads(request.body)
        registro= Usuarios.objects.filter(username=jd['username'])
        usuario_edit= list(Usuarios.objects.filter(usuario_id=id).values())
        if len(usuario_edit) > 0:

            # TO DO with serializers: user must pass in all fields

            registro = Usuarios.objects.get(usuario_id=id)
            registro.nombre=jd['nombre']
            registro.apellidos=jd['apellidos']
            registro.correo_electronico=jd['correo_electronico']
            registro.fecha_nacimiento=jd['fecha_nacimiento']
            registro.username=jd['username']
            registro.contrasena=jd['contrasena']
            registro.acerca_de_mi=jd['acerca_de_mi']
            registro.genero_id=jd['genero_id']


            # TODO: repeat for rest of skills
            # check entry is in Skills database
            s1 = jd['skill_1']
            if not s1.isnumeric():
                datos = {'codigo' : "400", 'message' : "Please enter numeric skill id"}
                return JsonResponse(datos)
            skill_1 = Habilidad.objects.filter(habilidad_id=s1)
            if not skill_1:
                datos = {'codigo' : "400", 'message' :  "Skill not found in database"}
                return JsonResponse(datos)
            skill_1 = Habilidad.objects.get(habilidad_id=s1)

            # check if user_id, skill_1 exists in usario_habilidad
            x = Usuario_habilidad.objects.filter(usuario_id=id, habilidad_id = registro.skill_1).values('usuario_habilidad_id').first()
            if not x:
                Usuario_habilidad.objects.create(usuario_id=id, habilidad_id=jd['skill_1'])
            else:
                registro_habilidades = Usuario_habilidad.objects.get(usuario_habilidad_id = x['usuario_habilidad_id'])
                registro_habilidades.usuario_id = id
                registro_habilidades.habilidad_id = jd['skill_1']
                registro_habilidades.save()

            registro.skill_1 = skill_1




            s2 = jd['skill_2']
            if not s2.isnumeric():
                datos = {'codigo' : "400", 'message' : "Please enter numeric skill id"}
                return JsonResponse(datos)
            skill_2 = Habilidad.objects.filter(habilidad_id=s2)
            if not skill_2:
                datos = {'codigo' : "400", 'message' :  "Skill not found in database"}
                return JsonResponse(datos)
            skill_2 = Habilidad.objects.get(habilidad_id=s2)

            x = Usuario_habilidad.objects.filter(usuario_id=id, habilidad_id = registro.skill_2).values('usuario_habilidad_id').first()
            if not x:
                Usuario_habilidad.objects.create(usuario_id=id, habilidad_id=jd['skill_2'])
            else:
                registro_habilidades = Usuario_habilidad.objects.get(usuario_habilidad_id = x['usuario_habilidad_id'])
                registro_habilidades.usuario_id = id
                registro_habilidades.habilidad_id = jd['skill_2']
                registro_habilidades.save()

            registro.skill_2 = skill_2

            registro.save()
            registro = list(Usuarios.objects.filter(correo_electronico=jd['correo_electronico']).values(  
            "nombre","apellidos","fecha_nacimiento","username","acerca_de_mi","correo_electronico",
            "skill_1", "skill_2", "skill_3", "skill_3", "skill_4", "skill_5"))
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
        if id != 0:
            habilidad = list(Usuario_habilidad.objects.prefetch_related('Habilidad').filter(usuario_id=id).values(
                "habilidad__habilidad_descripcion","habilidad__habilidad_id"
            ))
            if len(habilidad) > 0:
                informacion = habilidad
                datos = {'codigo':"200",'message': "Success", 'User skills': informacion}
                return JsonResponse(datos)
            else:
                datos = {'codigo':"400",'message': "Skills not found for this user..."}
                return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        registro = Usuario_habilidad.objects.filter(usuario_id=jd['usuario_id'])
        if len(registro) == 5:
            datos = {'codigo':"400",'message': "Solo debe elegir 5 habilidades"}  
            return JsonResponse(datos)
        registro = Usuario_habilidad.objects.filter(usuario_id=jd['usuario_id'],habilidad_id=jd['habilidad_id'])
        if len(registro) > 0:
            datos = {'codigo':"400",'message': "Habilidad previamente guardada"}  
            return JsonResponse(datos)
        else:
            skill = Habilidad.objects.filter(habilidad_id=jd['habilidad_id'])
            if not skill:
                datos = {'codigo':"400",'message': "Skill not found in database"}
                return JsonResponse(datos)
            skill = Habilidad.objects.get(habilidad_id=jd['habilidad_id'])
            user = Usuarios.objects.get(usuario_id=jd['usuario_id'])

            if user.skill_1 is None:
                Usuarios.objects.filter(usuario_id=jd['usuario_id']).update(skill_1=skill)
            elif user.skill_2 is None:
                Usuarios.objects.filter(usuario_id=jd['usuario_id']).update(skill_2=skill)
            elif user.skill_3 is None:
                Usuarios.objects.filter(usuario_id=jd['usuario_id']).update(skill_3=skill)
            elif user.skill_4 is None:
                Usuarios.objects.filter(usuario_id=jd['usuario_id']).update(skill_4=skill)
            elif user.skill_5 is None:
                Usuarios.objects.filter(usuario_id=jd['usuario_id']).update(skill_5=skill)

            Usuario_habilidad.objects.create(usuario_id=jd['usuario_id'], habilidad_id=jd['habilidad_id'])           

            datos = {'codigo':"201",'message': "Success"}
       
        return JsonResponse(datos)

    def delete(self, request, id):
        jd = json.loads(request.body)
        registro = Usuario_habilidad.objects.get(usuario_habilidad_id=id)
        user_skills_list = list(Usuario_habilidad.objects.filter(usuario_habilidad_id=id).values())
        if len(user_skills_list) > 0:

            user = Usuarios.objects.get(usuario_id=registro.usuario_id)
            skill_to_delete = Habilidad.objects.get(habilidad_id=registro.habilidad_id)

            if user.skill_1 == skill_to_delete:
                Usuarios.objects.filter(usuario_id=registro.usuario_id).update(skill_1=None)
            elif user.skill_2 == skill_to_delete:
                Usuarios.objects.filter(usuario_id=registro.usuario_id).update(skill_2=None)
            elif user.skill_3 == skill_to_delete:
                Usuarios.objects.filter(usuario_id=registro.usuario_id).update(skill_3=None)
            elif user.skill_4 == skill_to_delete:
                Usuarios.objects.filter(usuario_id=registro.usuario_id).update(skill_4=None)
            elif user.skill_5 == skill_to_delete:
                Usuarios.objects.filter(usuario_id=registro.usuario_id).update(skill_5=None)

            Usuario_habilidad.objects.filter(usuario_habilidad_id=id).delete()
            
            datos = {'codigo':"200",'message': "Success"}
        else:
            datos = {'codigo':"400",'message': "There is no entry with that ID"}
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

       

