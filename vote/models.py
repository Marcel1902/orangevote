from email.policy import default
from random import choices

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


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
    Rapide = 'Rapide'
    Moyenne = 'Moyenne'
    Lent = 'Lent'
    deploiment_choices = [
        (Rapide, 'Rapide'),
        (Moyenne, 'Moyenne'),
        (Lent, 'Lent'),
    ]
    name = models.CharField(max_length=255, unique=True)  # Nom unique pour la commune
    description = models.TextField(blank=True, null=True)  # Description optionnelle
    note_moyenne = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Note moyenne de la commune (calculée)
    site_brandes = models.IntegerField(default=0)
    repris_concurrence = models.IntegerField(default=0)
    rapidite_deploiement = models.CharField(max_length=25, choices=deploiment_choices, default=Moyenne)
    sous_zone = models.ForeignKey(SousZone, on_delete=models.CASCADE, related_name="communes")

    def __str__(self):
        return self.name

    from django.db.models import Sum

    def calculer_note_moyenne(self):
        # Calcul des votes via une annotation
        votes_data = self.votes.aggregate(
            total_qualite=Sum('qualite_site'),
            total_originalite=Sum('originalite_support')
        )
        total_notes_votes = (
                (votes_data['total_qualite'] or 0) +
                (votes_data['total_originalite'] or 0)
        )
        total_criteria_votes = self.votes.count() * 2  # 2 critères par vote

        # Calcul des critères spécifiques à la commune
        total_notes_commune = (
                self.site_brandes +
                self.repris_concurrence +
                self.get_rapidite_deploiement_value()
        )
        total_criteria_commune = 3  # Nombre de critères dans la commune

        # Calcul final
        total_notes = total_notes_votes + total_notes_commune
        total_criteria = total_criteria_votes + total_criteria_commune

        if total_criteria > 0:
            self.note_moyenne = round(total_notes / total_criteria, 2)
        else:
            self.note_moyenne = 0.0

        self.save()

    def get_rapidite_deploiement_value(self):
        """Convertit la valeur de 'rapidite_deploiement' en une valeur numérique."""
        if self.rapidite_deploiement == self.Rapide:
            return 5
        elif self.rapidite_deploiement == self.Moyenne:
            return 3
        elif self.rapidite_deploiement == self.Lent:
            return 1
        return 0  # Valeur par défaut si aucun choix n'est trouvé
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

        # Ajoutez ces propriétés pour récupérer les critères administratifs
        @property
        def site_brandes(self):
            return self.commune.site_brandes

        @property
        def repris_concurrence(self):
            return self.commune.repris_concurrence

        @property
        def rapidite_deploiement(self):
            return self.commune.rapidite_deploiement


