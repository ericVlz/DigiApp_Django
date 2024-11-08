from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from django.contrib.auth.models import Group
from django.contrib.auth.models import User



@receiver(post_save, sender=User)
def agregar_a_grupos_por_defecto(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            grupo_administradores, _ = Group.objects.get_or_create(name='Administradores')
            instance.groups.add(grupo_administradores)
        else:
            grupo_administradores, _ = Group.objects.get_or_create(name='Operativos')
            instance.groups.add(grupo_administradores)


@receiver(post_migrate)
def crear_grupos_y_permisos(sender, **kwargs):

    Group.objects.get_or_create(name='Administradores')
    Group.objects.get_or_create(name='Directivos')
    Group.objects.get_or_create(name='Operativos')
