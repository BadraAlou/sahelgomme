from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from .forms import RegisterForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from io import BytesIO
import os
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Vues générales
def accueil(request):
    return render(request, 'KidalApp/accueil.html')

def about(request):
    return render(request, 'KidalApp/about.html')

def contact(request):
    return render(request, 'KidalApp/contact.html')

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Produit, Categorie

def produit(request):
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        produits_list = Produit.objects.filter(categorie_id=categorie_id)
    else:
        produits_list = Produit.objects.all()

    paginator = Paginator(produits_list, 6)  # 6 produits par page
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)
    
    categories = Categorie.objects.all()
    return render(request, 'KidalApp/produit.html', {
        'produits': produits,
        'categories': categories,
        'selected_categorie': int(categorie_id) if categorie_id else None,
    })


def rechercher_produit(request):
    if 'q' in request.GET:
        query = request.GET['q']
        produits = Produit.objects.filter(nom__icontains=query)
    else:
        produits = Produit.objects.all()
    return render(request, 'KidalApp/rechercher_produit.html', {'produits': produits})

# Vues pour l'authentification

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            subject = 'Bienvenue sur notre site'
            message = f'Bonjour {user.username},\n\nMerci de vous être connecte sur notre site. Nous espérons que vous apprécierez votre expérience.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('accueil')
        else:
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return render(request, 'KidalApp/login.html', {'error_message': error_message})
    return render(request, 'KidalApp/login.html')
def logout_user(request):
    logout(request)
    return redirect('accueil')

from django.core.mail import send_mail
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Utilisez set_password pour sécuriser le mot de passe
            user.save()
            login(request, user)  # Connectez automatiquement l'utilisateur après l'inscription

            # Envoyer un email de bienvenue
            subject = 'Bienvenue sur notre site'
            message = f'Bonjour {user.username},\n\nMerci de vous être inscrit sur notre site. Nous espérons que vous apprécierez votre expérience.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, 'Vous êtes maintenant inscrit.')
            return redirect('accueil')
    else:
        form = RegisterForm()
    return render(request, 'KidalApp/register.html', {'form': form})


# Vues pour le panier


# Vues pour les commandes
def commander_produit(request, produit_id):
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite'))
        mode_paiement = request.POST.get('mode_paiement')
        produit = Produit.objects.get(id=produit_id)
        if produit.stock >= quantite:
            commande = Commande.objects.create(
                produit=produit,
                utilisateur=request.user if request.user.is_authenticated else None,
                quantite=quantite,
                mode_paiement=mode_paiement
            )
            produit.stock -= quantite
            produit.save()
             # Envoyer un email de confirmation de commande
            subject = 'Confirmation de votre commande'
            message = f'Bonjour {request.user.username},\n\nVotre commande pour le produit {produit.nom} a été passée avec succès.\nQuantité : {quantite}\nMode de paiement : {commande.get_mode_paiement_display()}\n\nMerci pour votre achat.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'Votre commande a été passée avec succès!')
            return redirect('confirmation_commande', commande_id=commande.id)
        messages.error(request, 'Le produit est en rupture de stock.')
        return redirect('produit')
    produit = Produit.objects.get(id=produit_id)
    return render(request, 'KidalApp/commande.html', {'produit': produit})

def confirmation_commande(request, commande_id):
    commande = Commande.objects.get(id=commande_id)
    prix_total = commande.quantite * commande.produit.prix
    return render(request, 'KidalApp/confirmation_commande.html', {'commande': commande, 'prix_total': prix_total})

def generate_invoice_pdf(request, commande_id):
    commande = Commande.objects.get(id=commande_id)
    produit = commande.produit
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', parent=styles['Heading1'], fontSize=24, leading=28, spaceAfter=14, alignment=1)
    normal_style = styles['Normal']
    footer_style = ParagraphStyle('footer', parent=styles['Normal'], fontSize=10, textColor=colors.grey, alignment=1)

    logo_path = os.path.join('KidalApp', 'static', 'img', 'logo1.jpeg')  # Remplacez par le chemin de votre logo
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=4 * cm, height=4 * cm)
        elements.append(logo)
        elements.append(Spacer(1, 1 * cm))

    company_info = Paragraph("""
        <b>Sahel Gomme</b><br/>
        Sebenicoro<br/>
        Bamako, 99335<br/>
        Téléphone: +223 83 45 15 13<br/>
        Email: sahelgomme@gmail.com
    """, normal_style)
    elements.append(company_info)
    elements.append(Spacer(1, 1 * cm))

    user = request.user
    user_name = user.get_full_name() or user.username
    user_info = Paragraph(f"Client: {user_name}", normal_style)
    elements.append(user_info)
    elements.append(Spacer(1, 0.5 * cm))

    title = Paragraph(f"Facture pour la commande num #{commande.id}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.5 * cm))

    data = [
        ['Produit', produit.nom],
        ['Description', f"{produit.description} Kg"],
        ['Quantité', commande.quantite],
        ['Prix unitaire', f"{produit.prix} FCFA"],
        ['Prix total', f"{commande.quantite * produit.prix} FCFA"],
        ['Mode de paiement', commande.get_mode_paiement_display()],
    ]

    table = Table(data, colWidths=[7 * cm, 10 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 2 * cm))

    footer = Paragraph("Merci pour votre achat!", footer_style)
    elements.append(footer)

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{commande.id}.pdf"'
    response.write(pdf)
    return response

# Vues de contact
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Panier, PanierItem, CommanderPanier, Produit, Commande

@login_required
def gerer_panier(request):
    panier, created = Panier.objects.get_or_create(utilisateur=request.user)
    items = panier.items.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        produit_id = request.POST.get('produit_id')

        if action and produit_id:
            item = get_object_or_404(PanierItem, id=int(produit_id))

            if action == 'modifier_quantite':
                nouvelle_quantite = int(request.POST.get('quantite'))
                if nouvelle_quantite > 0:
                    item.quantite = nouvelle_quantite
                    item.save()
                    messages.success(request, f"La quantité de {item.produit.nom} a été mise à jour.")
                else:
                    messages.error(request, "La quantité doit être supérieure à zéro.")

            elif action == 'supprimer':
                item.delete()
                messages.success(request, f"{item.produit.nom} a été supprimé du panier.")

            elif action == 'commander_panier':
                return commander_panier(request)

            return redirect('gerer_panier')

        else:
            messages.error(request, "Action non valide ou ID de produit manquant.")

    context = {
        'panier': panier,
        'items': items,
    }
    return render(request, 'KidalApp/gerer_panier.html', context)


@login_required
def commander_panier(request):
    panier = Panier.objects.get(utilisateur=request.user)
    mode_paiement = '1'  # Vous pouvez ajuster le mode de paiement selon vos besoins

    commande = CommanderPanier.objects.create(
        panier=panier,
        utilisateur=request.user,
        mode_paiement=mode_paiement
    )

    for item in panier.items.all():
        # Créer une commande pour chaque article dans le panier
        Commande.objects.create(
            produit=item.produit,
            utilisateur=request.user,
            quantite=item.quantite,
            mode_paiement=mode_paiement
        )

    panier.items.all().delete()
 # Envoyer un email de confirmation de commande
    subject = 'Confirmation de votre commande'
    message = f'Bonjour {request.user.username},\n\nVotre commande pour le produit {item.produit.nom} a été passée avec succès.\n\nMerci pour votre achat.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email]
    send_mail(subject, message, from_email, recipient_list)    
    messages.success(request, 'Votre commande a été passée avec succès!')

    # Redirection vers la page de confirmation de la commande avec l'ID de la commande créée
    return redirect('confirmationn_commande', commande_id=commande.id)
from django.shortcuts import render, get_object_or_404
from .models import CommanderPanier, PanierItem

@login_required
def confirmationn_commande(request, commande_id):
    # Récupérer la commande à partir de son ID
    commande_panier = get_object_or_404(CommanderPanier, id=commande_id)
    
    # Récupérer tous les items du panier associé à cette commande
    panier_items = PanierItem.objects.filter(panier=commande_panier.panier)

    context = {
        'commande_panier': commande_panier,
        'panier_items': panier_items,
    }

    return render(request, 'KidalApp/confirmationn_commande.html', context)

@login_required
def ajouter_au_panier(request, produit_id):
    panier, created = Panier.objects.get_or_create(utilisateur=request.user)
    produit = get_object_or_404(Produit, id=produit_id)

    item, created = PanierItem.objects.get_or_create(panier=panier, produit=produit)

    if not created:
        item.quantite += 1
        item.save()

    messages.success(request, f"{produit.nom} a été ajouté à votre panier.")
    return redirect('gerer_panier')


from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from ExamenApp.models import Employe, Absence, Paiement, Conge
from KidalApp.models import Produit, Commande

@staff_member_required
def dashboard(request):
    employe_count = Employe.objects.count()
    absence_count = Absence.objects.count()
    paiement_count = Paiement.objects.count()
    conge_count = Conge.objects.count()
    produit_count = Produit.objects.count()
    commande_count = Commande.objects.count()

    context = {
        'employe_count': employe_count,
        'absence_count': absence_count,
        'paiement_count': paiement_count,
        'conge_count': conge_count,
        'produit_count': produit_count,
        'commande_count': commande_count,
    }
    return render(request, 'admin/dashboard.html', context)
