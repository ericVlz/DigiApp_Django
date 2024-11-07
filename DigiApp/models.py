from django.db import models
from django.contrib.auth.models import User


def custom_filename(instance, filename):
    new_filename = str(instance.propietario) + '_' + str(instance.nombre)
    ext = filename.split('.')[-1]
    return 'documentos/{}.{}'.format(new_filename,ext)



class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Documento(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to=custom_filename)
    contenido = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='documentos')

    def __str__(self):
        return self.nombre
    