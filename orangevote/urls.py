from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from vote.views import commune, detail_commune, vote_commune, rechercher_commune, connexion, deconnexion, liste_zones, liste_sous_zones

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', connexion, name='connexion'), # Nouvelle route pour la connexion
    path('logout/', deconnexion, name='logout'),
    path('zones/', liste_zones, name='liste_zones'),# Nouvelle route pour la liste des zones
    path('zones/<int:zone_id>/', liste_sous_zones, name='liste_sous_zones'), # Nouvelle route pour la liste des sous-zones liées à une zone
    path('sous-zones/<int:sous_zone_id>/', commune, name='liste_communes'),
    path('communes/<int:commune_id>/', detail_commune, name='detail_commune'),
    path('communes/<int:commune_id>/vote/', vote_commune, name='vote_commune'),
    path('communes/rechercher/', rechercher_commune, name='rechercher_commune'),
]
if settings.DEBUG:  # Servir les fichiers médias seulement en mode DEBUG
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
