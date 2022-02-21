from django.db import models

# Create your models here.
 
class Usuarios(models.Model):
    usuario_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='ID')
    nombre = models.CharField(max_length=100)
    apellidos =models.CharField(max_length=100)
    fecha_nacimiento=models.DateField()
    genero_id=models.IntegerField(null=True)
    correo_electronico =models.CharField(max_length=100)
    username =models.CharField(max_length=100)
    contrasena =models.CharField(max_length=250)
    contrasena =models.CharField(max_length=250)
    acerca_de_mi =models.CharField(max_length=250)


