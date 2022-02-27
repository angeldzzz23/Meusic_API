from django.db import models
from  api.models import * 

class Usuarios(models.Model):
    usuario_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='usuario_id')
    nombre = models.CharField(max_length=100)
    apellidos =models.CharField(max_length=100)
    fecha_nacimiento=models.DateField()
    genero =models.ForeignKey(Genero, on_delete=models.CASCADE,verbose_name='genero_id')
    correo_electronico =models.CharField(max_length=100)
    username =models.CharField(max_length=100)
    contrasena =models.CharField(max_length=250)
    contrasena =models.CharField(max_length=250)
    fecha_creacion_usuario=models.DateField()
    acerca_de_mi =models.CharField(max_length=250)
    class Meta:
        db_table = 'usuarios'
