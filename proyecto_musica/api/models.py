from django.db import models

# Create your models here.


class Genero(models.Model):
    genero_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='genero_id')
    genero_descripcion = models.CharField(max_length=200)
    def __str__(self):
        return self.genero_id
    class Meta:
        db_table = 'Genero'
 
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
    fecha_creacion=models.DateField(auto_now=False,auto_now_add=True)
    acerca_de_mi =models.CharField(max_length=250)
    def __str__(self):
        return self.usuario_id
    class Meta:
        db_table = 'usuarios'

class usuario_artista(models.Model):
    usuario_artista_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='usuario_artista_id')
    usuario =models.ForeignKey(Usuarios, on_delete=models.CASCADE,verbose_name='usuario_id')
    artista_id = models.CharField(max_length=100)
   
    class Meta:
        db_table = 'usuario_artista'







