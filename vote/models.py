from django.db import models

# Create your models here.
class Commune(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Nom unique pour la commune
    description = models.TextField(blank=True, null=True)  # Description optionnelle
    note_moyenne = models.FloatField(default=0.0)  # Note moyenne de la commune (calculée)

    def __str__(self):
        return self.name

    def calculer_note_moyenne(self):
        """Met à jour la note moyenne basée sur les votes."""
        votes = self.votes.all()  # Récupère tous les votes associés à cette commune
        if votes.exists():
            self.note_moyenne = sum(vote.note for vote in votes) / votes.count()
        else:
            self.note_moyenne = 0.0
        self.save()

class Image(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')  # Chemin de stockage des images
    description = models.TextField(blank=True, null=True)  # Description optionnelle de l'image
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout de l'image

    def __str__(self):
        return f"Image de {self.commune.name}"

from django.contrib.auth.models import User  # Pour les utilisateurs qui votent

class Vote(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')  # Un utilisateur peut voter
    note = models.PositiveSmallIntegerField()  # Note, par exemple de 1 à 5
    created_at = models.DateTimeField(auto_now_add=True)  # Date du vote

    class Meta:
        unique_together = ('commune', 'user')  # Empêche un utilisateur de voter plusieurs fois pour la même commune

    def __str__(self):
        return f"Vote de {self.user.username} pour {self.commune.name}: {self.note}"

