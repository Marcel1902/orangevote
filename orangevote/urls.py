from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from vote.views import commune, detail_commune, vote_commune, rechercher_commune, connexion, deconnexion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', connexion, name='connexion'), # Nouvelle route pour la connexion
    path('logout/', deconnexion, name='logout'),
    path('communes/', commune, name='liste_communes'),
    path('communes/<int:commune_id>/', detail_commune, name='detail_commune'),
    path('communes/<int:commune_id>/vote/', vote_commune, name='vote_commune'),
    path('communes/rechercher/', rechercher_commune, name='rechercher_commune'),
]
if settings.DEBUG:  # Servir les fichiers médias seulement en mode DEBUG
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
