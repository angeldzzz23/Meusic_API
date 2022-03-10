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

class Usuario_artista(models.Model):
    usuario_artista_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='usuario_artista_id')
    usuario =models.ForeignKey(Usuarios, on_delete=models.CASCADE,verbose_name='usuario_id')
    artista_id = models.CharField(max_length=100)
   
    class Meta:
        db_table = 'usuario_artista'

class Habilidad(models.Model):
    habilidad_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='habilidad_id')
    habilidad_descripcion =models.CharField(max_length=200)

    def __str__(self):
        return self.habilidad_id
    class Meta:
        db_table = 'habilidad'

class Usuario_habilidad(models.Model):
    usuario_habilidad_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='Usuario_habilidad_id')
    usuario =models.ForeignKey(Usuarios, on_delete=models.CASCADE,verbose_name='usuario_id')
    habilidad =models.ForeignKey(Habilidad, on_delete=models.CASCADE,verbose_name='habilidad_id')
   
    class Meta:
        db_table = 'Usuario_habilidad'

class Genero_musical(models.Model):
    genero_musical_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='genero_musical_id')
    genero_musical_descripcion =models.CharField(max_length=200)

    def __str__(self):
        return self.genero_musical_id
    class Meta:
        db_table = 'genero_musical'

class Usuario_genero_musical(models.Model):
    usuario_genero_musical_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='usuario_genero_musical_id')
    usuario =models.ForeignKey(Usuarios, on_delete=models.CASCADE,verbose_name='usuario_id')
    genero_musical =models.ForeignKey(Genero_musical, on_delete=models.CASCADE,verbose_name='genero_musical_id')
   
    class Meta:
        db_table = 'usuario_genero_musical'







