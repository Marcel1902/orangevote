from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Vote

@receiver(post_save, sender=Vote)
@receiver(post_delete, sender=Vote)
def update_commune_note_moyenne(sender, instance, **kwargs):
    instance.commune.calculer_note_moyenne()
