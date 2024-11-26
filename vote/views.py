from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
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
        # Récupère la commune en fonction de son ID
        commune = get_object_or_404(Commune, id=commune_id)
        note = request.POST.get('rating')

        if note and note.isdigit():
            note = int(note)
            if 1 <= note <= 5:
                # Vérifier si l'utilisateur a déjà voté pour cette commune
                if Vote.objects.filter(commune=commune, user=request.user).exists():
                    messages.error(request, "Vous avez déjà voté pour cette commune.")
                else:
                    # Créer un nouveau vote pour l'utilisateur connecté
                    Vote.objects.create(commune=commune, note=note, user=request.user)
                    # Recalcule la note moyenne de la commune après le vote
                    commune.calculer_note_moyenne()
                    messages.success(request, 'Votre vote a été enregistré.')
            else:
                messages.error(request, 'La note doit être comprise entre 1 et 5.')
        else:
            messages.error(request, 'Vote invalide.')
        print(f"Note moyenne après le calcul: {commune.note_moyenne}")  # Debugging line

        return redirect('detail_commune', commune_id=commune.id)
@login_required
def rechercher_commune(request):
    query = request.GET.get('q', '')
    communes = Commune.objects.filter(name__icontains=query) if query else Commune.objects.all()
    return render(request, 'vote/liste_communes.html', {'communes': communes, 'query': query})
