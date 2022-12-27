from account.auth_backends import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Code


@receiver(post_save, sender=User)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
        Code.objects.create(user=instance)
