from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from django.contrib.auth.models import Group
from django.contrib.auth.models import User



@receiver(post_save, sender=User)
def agregar_superusuario_a_administradores(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        grupo_administradores, _ = Group.objects.get_or_create(name='Administradores')
        instance.groups.add(grupo_administradores)


@receiver(post_migrate)
def crear_grupos_y_permisos(sender, **kwargs):

    Group.objects.get_or_create(name='Administradores')
    Group.objects.get_or_create(name='Directivos')
    Group.objects.get_or_create(name='Operativos')
