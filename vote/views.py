from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from openpyxl.styles import Alignment
from openpyxl.workbook import Workbook

from .models import Vote, Image, Commune
# Create your views here.

def connexion(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            # Authentifie l'utilisateur et redirige vers la page d'accueil
            login(request, user)
            return redirect('liste_communes')
        else:
            # Erreur d'authentification
            messages.error(request, "Identifiants invalides.")
    return render(request, 'vote/index.html')

@login_required
def deconnexion(request):
    # Déconnecte l'utilisateur et redirige vers la page de connexion
    logout(request)
    return redirect('connexion')

@login_required
def commune(request):
    communes = Commune.objects.all()
    return render(request, 'vote/liste_communes.html', {'communes':communes})

@login_required
def detail_commune(request, commune_id):
    commune = get_object_or_404(Commune, id=commune_id)
    commune.calculer_note_moyenne()
    return render(request, 'vote/detail_commune.html', {'commune': commune})


@login_required
def vote_commune(request, commune_id):
    if request.method == 'POST':
        commune = get_object_or_404(Commune, id=commune_id)

        try:
            qualite_site = int(request.POST.get('qualite_site', 0))
            originalite_support = int(request.POST.get('originalite_support', 0))

            # Validation des données
            if not (1 <= qualite_site <= 5 and 1 <= originalite_support <= 5):
                raise ValueError("Les notes doivent être entre 1 et 5.")

            # Vérification si l'utilisateur a déjà voté
            if Vote.objects.filter(commune=commune, user=request.user).exists():
                messages.warning(request, "Vous avez déjà voté pour cette commune.")
            else:
                # Création du vote
                Vote.objects.create(
                    commune=commune,
                    user=request.user,
                    qualite_site=qualite_site,
                    originalite_support=originalite_support,
                )
                # Recalcul de la note moyenne
                commune.calculer_note_moyenne()
                messages.success(request, "Votre vote a été enregistré.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('detail_commune', commune_id=commune.id)


@login_required
def rechercher_commune(request):
    query = request.GET.get('q', '')
    communes = Commune.objects.filter(name__icontains=query) if query else Commune.objects.all()
    return render(request, 'vote/liste_communes.html', {'communes': communes, 'query': query})
