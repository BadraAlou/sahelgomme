from django.shortcuts import render

# Create your views here.
from .models import *
# Create your views here.
def accueil(request):
    return render(request, 'KidalApp/accueil.html')


from django.contrib.auth.decorators import login_required


def produit(request):
    produits = Produit.objects.all()
    return render(request, 'KidalApp/produit.html', {'produits': produits})




def rechercher_produit(request):
    if 'q' in request.GET:
        query = request.GET['q']
        produits = Produit.objects.filter(nom__icontains=query)
    else:
        produits = Produit.objects.all()
    return render(request, 'KidalApp/rechercher_produit.html', {'produits': produits})




from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Produit, Panier, Commande, Message
from .forms import RegisterForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login  # Ajoutez ceci
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Produit, Panier, CustomUser
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return render(request, 'KidalApp/login.html', {'error_message': 'Nom d\'utilisateur ou mot de passe incorrect.'})
    else:
        return render(request, 'KidalApp/login.html')



from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    return redirect('accueil')

from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Utilisez set_password pour sécuriser le mot de passe
            user.save()
            login(request, user)  # Connectez automatiquement l'utilisateur après l'inscription
            messages.success(request, 'Vous êtes maintenant inscrit.')
            return redirect('accueil')
    else:
        form = RegisterForm()
    return render(request, 'KidalApp/register.html', {'form': form})



from django.shortcuts import redirect
from .models import Produit, Panier


from .models import Panier

def panier(request):
    if request.user.is_authenticated:
        panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
        produits = panier.produits.all()
        return render(request, 'KidalApp/panier.html', {'produits': produits})
    else:
        return redirect('login')  # Redirigez l'utilisateur vers la page de connexion s'il n'est pas connecté


from django.shortcuts import render, redirect
from .models import Panier, Produit
from django.shortcuts import render, redirect
from .models import Panier, Produit
def ajouter_au_panier(request):
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        quantite = int(request.POST.get('quantite', 1))  # Ajout de la quantité
        produit = Produit.objects.get(pk=produit_id)
        if request.user.is_authenticated:
            panier, created = Panier.objects.get_or_create(utilisateur=request.user)
            panier.produits.add(produit, through_defaults={'quantite': quantite})  # Ajout de la quantité
            return redirect('panier')
        else:
            return redirect('login')
    else:
        return redirect('accueil')


from django.shortcuts import redirect
from .models import Panier

def supprimer_panier(request):
    if request.user.is_authenticated:
        # Récupérer le panier de l'utilisateur s'il existe
        panier = Panier.objects.filter(utilisateur=request.user).first()
        if panier:
            # Supprimer le panier
            panier.delete()
    # Rediriger l'utilisateur vers une page après la suppression du panier
    return redirect('accueil')  # Rediriger vers la page d'accueil par exemple


def confirmation_commande(request):
    return render(request, 'KidalApp/confirmation_commande.html')

from django.shortcuts import render, redirect
from .models import Produit, Commande
from django.contrib import messages
def commander_produit(request, produit_id):
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        mode_paiement = int(request.POST.get('mode_paiement', 1))  # Récupérer le mode de paiement sélectionné
        produit = Produit.objects.get(id=produit_id)

        # Vérifier si le produit est disponible en quantité suffisante
        if produit.stock >= quantite:
            # Créer une commande
            commande = Commande.objects.create(
                produit=produit,
                utilisateur=request.user if request.user.is_authenticated else None,
                quantite=quantite
            )

            # Réduire le stock du produit
            produit.stock -= quantite
            produit.save()

            messages.success(request, 'Votre commande a été passée avec succès!')
            return redirect('confirmation_commande')  # Rediriger l'utilisateur vers le panier

        else:
            messages.error(request, 'Le produit est en rupture de stock.')
            return redirect('produit')  # Rediriger l'utilisateur vers la liste des produits

    # Si la méthode HTTP n'est pas POST, afficher le formulaire de commande
    produit = Produit.objects.get(id=produit_id)
    return render(request, 'KidalApp/commande.html', {'produit': produit})


def conf(request):
    return render(request, 'KidalApp/conf.html')
@login_required
def contactez_nous(request):
    if request.method == 'POST':
        contenu = request.POST.get('contenu', '')
        if contenu:
            message = Message.objects.create(utilisateur=request.user, contenu=contenu)
            message.save()
            return redirect('conf')  # Rediriger vers la page d'accueil après l'envoi du message
    return render(request, 'KidalApp/contactez_nous.html')

def conf(request):
    return render(request, 'KidalApp/conf.html')


def my_page(request):
    return render(request, 'histoire.html')