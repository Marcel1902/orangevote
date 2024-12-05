from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect


from .models import Vote, Image, Commune, Zone, SousZone


# Create your views here.

def connexion(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            # Authentifie l'utilisateur et redirige vers la page d'accueil
            login(request, user)
            return redirect('liste_zones')
        else:
            # Erreur d'authentification
            messages.error(request, "Identifiants invalides.")
    return render(request, 'vote/index.html')

@login_required
def deconnexion(request):
    # Déconnecte l'utilisateur et redirige vers la page de connexion
    logout(request)
    return redirect('connexion')

def liste_zones(request):
    zones = Zone.objects.all()
    return render(request, 'vote/liste_zones.html', {'zones': zones})

def liste_sous_zones(request, zone_id):
    zone = get_object_or_404(Zone, id=zone_id)
    sous_zones = zone.souszones.all()
    return render(request, 'vote/liste_sous_zones.html', {'zone': zone, 'sous_zones': sous_zones})

@login_required
def commune(request, sous_zone_id):
    sous_zone = get_object_or_404(SousZone, id=sous_zone_id)
    communes = sous_zone.communes.all()
    paginator = Paginator(communes, 6)
    page_number = request.GET.get('page')  # Récupérer la page actuelle
    page_obj = paginator.get_page(page_number)
    return render(request, 'vote/liste_communes.html', {'communes':communes, 'page_obj': page_obj, 'sous_zone': sous_zone})




@login_required
def detail_commune(request, commune_id):
    commune = get_object_or_404(Commune, id=commune_id)
    all_images = commune.images.all()

    # Grouper les images par emplacement
    images_par_emplacement = []
    for image in all_images:
        emplacement = image.emplacement
        # Chercher si l'emplacement existe déjà dans la liste
        existing_entry = next((entry for entry in images_par_emplacement if entry[0] == emplacement), None)

        if not existing_entry:
            # Ajouter un nouvel emplacement avec des listes vides pour avant et après
            images_par_emplacement.append([emplacement, [], []])
            existing_entry = images_par_emplacement[-1]

        # Ajouter l'image à la bonne catégorie (avant ou après)
        if image.type_image == 'avant':
            existing_entry[1].append(image)
        elif image.type_image == 'apres':
            existing_entry[2].append(image)

    # Pagination des emplacements (2 par page)
    paginator = Paginator(images_par_emplacement, 2)  # 2 emplacements par page
    page_number = request.GET.get('page')  # Récupérer la page actuelle
    page_obj = paginator.get_page(page_number)

    commune.calculer_note_moyenne()

    return render(request, 'vote/detail_commune.html', {
        'commune': commune,
        'page_obj': page_obj,  # Passer l'objet de page
    })


@login_required
def vote_commune(request, commune_id):
    if request.method == 'POST':
        commune = get_object_or_404(Commune, id=commune_id)

        try:
            qualite_site = int(request.POST.get('qualite_site', 0))
            originalite_support = int(request.POST.get('originalite_support', 0))
            site_brandes = int(request.POST.get('site_brandes', 0))
            repris_concurrence = int(request.POST.get('repris_concurrence', 0))
            rapidite_deploiement = int(request.POST.get('rapidite_deploiement', 0))

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
                    site_brandes = site_brandes,
                    repris_concurrence = repris_concurrence,
                    rapidite_deploiement = rapidite_deploiement,
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
