from django.contrib import admin
from vote.models import Vote, Commune, Image

# Register your models here.
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_votes', 'note_moyenne')  # Ajouter 'total_votes' et 'note_moyenne'

    # Fonction pour calculer le total des votes pour chaque commune
    def total_votes(self, obj):
        return obj.votes.count()  # `votes` est la relation définie par `related_name='votes'` dans le modèle Vote

    total_votes.admin_order_field = 'votes__count'  # Permet de trier par total_votes dans l'admin
    total_votes.short_description = 'Total des votes'  # Texte affiché dans l'admin

    def note_moyenne(self, obj):
        # Calcul de la note moyenne, en utilisant les votes associés à la commune
        total_votes = obj.votes.count()
        if total_votes > 0:
            total_notes = sum(vote.note for vote in obj.votes.all())  # Somme de toutes les notes
            return total_notes / total_votes  # Moyenne des notes
        return 0

    note_moyenne.short_description = 'Note moyenne'

admin.site.register(Vote)
admin.site.register(Commune, CommuneAdmin)
admin.site.register(Image)
