from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Zone(models.Model):
    nom = models.CharField(max_length=255)  # Nom de la zone
    image = models.ImageField(upload_to='images/')

    def calculer_score_zone(self):
        """Calcule le score total d'une zone en additionnant les scores de ses sous-zones."""
        sous_zones = self.souszones.all()
        total_score = sum(sous_zone.calculer_score_sous_zone() for sous_zone in sous_zones)
        return total_score

    def __str__(self):
        return self.nom

class SousZone(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Nom de la sous-zone
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="souszones")
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

    def calculer_score_sous_zone(self):
        """Calcule le score d'une sous-zone en fonction des communes."""
        communes = self.communes.all()
        total_score = sum(commune.note_moyenne for commune in communes)
        return total_score

class Commune(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Nom unique pour la commune
    description = models.TextField(blank=True, null=True)  # Description optionnelle
    note_moyenne = models.FloatField(default=0.0)  # Note moyenne de la commune (calculée)
    sous_zone = models.ForeignKey(SousZone, on_delete=models.CASCADE, related_name="communes")

    def __str__(self):
        return self.name


    def calculer_note_moyenne(self):
        """
        Met à jour la note moyenne de la commune basée sur les votes,
        en prenant en compte les critères calculés.
        """
        votes = self.votes.all()  # Récupère tous les votes associés à cette commune
        if votes.exists():
            total_notes = sum(
                vote.qualite_site + vote.originalite_support
                for vote in votes
            )
            self.note_moyenne = total_notes / votes.count()
        else:
            self.note_moyenne = 0.0
        self.save()

class Image(models.Model):
    AVANT = 'avant'
    APRES = 'apres'
    TYPE_IMAGE_CHOICES = [
        (AVANT, 'Avant'),
        (APRES, 'Après'),
    ]
    type_image = models.CharField(max_length=5, choices=TYPE_IMAGE_CHOICES)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
    emplacement = models.CharField(max_length=100, help_text="Nom de l'emplacement, ex : Gymnase, École")
    description = models.TextField(blank=True, null=True)  # Description optionnelle de l'image
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout de l'image

    def __str__(self):
        return f"image {self.get_type_image_display()} du {self.emplacement} - {self.commune.name}"


class Vote(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')  # Un utilisateur peut voter
    qualite_site = models.PositiveSmallIntegerField(default=0)  # Qualité des sites (1-5)
    originalite_support = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Date du vote

    class Meta:
        unique_together = ('commune', 'user')  # Empêche un utilisateur de voter plusieurs fois pour la même commune

    def __str__(self):
        return f"Vote de {self.user.username} pour {self.commune.name}"


