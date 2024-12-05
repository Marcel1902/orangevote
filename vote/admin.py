from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment
from vote.models import Commune, Vote, Zone, SousZone, Image


# Fonction d'exportation des résultats
def export_vote_results(modeladmin, request, queryset):
    if not request.user.is_superuser:
        return HttpResponse("Vous n'avez pas les permissions nécessaires pour effectuer cette action.")

    # Créer un nouveau classeur Excel
    wb = Workbook()

    # Feuille des résultats des communes
    ws_commune = wb.active
    ws_commune.title = "Résultats des Communes"
    headers_commune = ['Commune', 'Qualité du Site', 'Originalité du Support', 'site_brandes', 'repris_concurrence', 'rapidite_deploiement', 'Total']
    ws_commune.append(headers_commune)

    # Appliquer un alignement centré aux en-têtes de la feuille commune
    for cell in ws_commune[1]:
        cell.alignment = Alignment(horizontal='center')

    # Résultats des communes regroupés
    commune_results = {}

    for commune in queryset:
        if commune.name not in commune_results:
            commune_results[commune.name] = {'qualite_site': 0, 'originalite_support': 0, 'site_brandes': 0, 'repris_concurrence': 0, 'rapidite_deploiement':0}

        for vote in commune.votes.all():
            commune_results[commune.name]['qualite_site'] += vote.qualite_site
            commune_results[commune.name]['originalite_support'] += vote.originalite_support
            commune_results[commune.name]['site_brandes'] += vote.site_brandes
            commune_results[commune.name]['repris_concurrence'] += vote.repris_concurrence
            commune_results[commune.name]['rapidite_deploiement'] += vote.rapidite_deploiement

    # Ajout des données regroupées dans la feuille Excel
    for commune_name, results in commune_results.items():
        total_notes = results['qualite_site'] + results['originalite_support'] + results['site_brandes'] + results['repris_concurrence'] +results['rapidite_deploiement']
        row = [
            commune_name,
            results['qualite_site'],  # Total Qualité du Site
            results['originalite_support'], # Total Originalité du Support
            results['site_brandes'],
            results['repris_concurrence'],
            results['rapidite_deploiement'],  # Total Rapideté de Déploiement
            total_notes,  # Total général
        ]
        ws_commune.append(row)

    # Feuille des résultats des sous-zones
    ws_sous_zone = wb.create_sheet(title="Résultats des Sous-Zones")
    headers_sous_zone = ['Sous-zone', 'Qualité du Site', 'Originalité du Support', 'site_brandes', 'repris_concurrence', 'rapidite_deploiement', 'Total']
    ws_sous_zone.append(headers_sous_zone)

    for souszone in SousZone.objects.all():
        total_qualite_site = 0
        total_originalite_support = 0
        total_site_brandes = 0
        total_repris_concurrence = 0
        total_rapidite_deploiement = 0

        # Récupérer les communes liées à cette sous-zone
        for commune in souszone.communes.all():
            for vote in commune.votes.all():
                total_qualite_site += vote.qualite_site
                total_originalite_support += vote.originalite_support
                total_site_brandes += vote.site_brandes
                total_repris_concurrence += vote.repris_concurrence
                total_rapidite_deploiement += vote.rapidite_deploiement

        total_notes = total_qualite_site + total_originalite_support + total_site_brandes + total_repris_concurrence + total_rapidite_deploiement
        row = [souszone.name, total_qualite_site, total_originalite_support, total_site_brandes, total_repris_concurrence, total_rapidite_deploiement, total_notes]
        ws_sous_zone.append(row)

    # Feuille des résultats des zones
    ws_zone = wb.create_sheet(title="Résultats des Zones")
    headers_zone = ['Zone', 'Qualité du Site', 'Originalité du Support', 'site_brandes', 'repris_concurrence', 'rapidite_deploiement', 'Total']
    ws_zone.append(headers_zone)

    for zone in Zone.objects.all():
        total_qualite_site = 0
        total_originalite_support = 0
        total_site_brandes = 0
        total_repris_concurrence = 0
        total_rapidite_deploiement = 0

        # Récupérer les sous-zones liées à cette zone
        for souszone in zone.souszones.all():
            for commune in souszone.communes.all():
                for vote in commune.votes.all():
                    total_qualite_site += vote.qualite_site
                    total_originalite_support += vote.originalite_support
                    total_site_brandes += vote.site_brandes
                    total_repris_concurrence += vote.repris_concurrence
                    total_rapidite_deploiement += vote.rapidite_deploiement

        total_notes = total_qualite_site + total_originalite_support + total_site_brandes + total_repris_concurrence + total_rapidite_deploiement
        row = [zone.nom, total_qualite_site, total_originalite_support, total_site_brandes, total_repris_concurrence, total_rapidite_deploiement,  total_notes]
        ws_zone.append(row)

    # Créer la réponse HTTP pour télécharger le fichier Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="resultats_votes.xlsx"'

    wb.save(response)
    return response


class CommuneAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_votes', 'note_moyenne')
    actions = [export_vote_results]

    def total_votes(self, obj):
        return obj.votes.count()

    total_votes.admin_order_field = 'votes__count'
    total_votes.short_description = 'Total des votes'

    def note_moyenne(self, obj):
        total_votes = obj.votes.count()
        if total_votes > 0:
            total_notes = sum(vote.qualite_site + vote.originalite_support for vote in obj.votes.all())
            return total_notes / (total_votes * 2)  # Divisé par 2 car il y a deux critères
        return 0

    note_moyenne.short_description = 'Note moyenne'


# Enregistrer les modèles dans l'admin
admin.site.register(Commune, CommuneAdmin)
admin.site.register(Zone)
admin.site.register(SousZone)
admin.site.register(Vote)
admin.site.register(Image)
