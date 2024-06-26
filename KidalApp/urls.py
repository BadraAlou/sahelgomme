from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import dashboard

urlpatterns = [
    path('', views.accueil, name='accueil'),
        path('produit/', views.produit, name='produit'),
                path('about/', views.about, name='about'),
                                path('contact/', views.contact, name='contact'),
 path('recherche/', views.rechercher_produit, name='recherche_produit'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('commander/<int:produit_id>/', views.commander_produit, name='commander_produit'), # Ajoutez ce chemin pour la commande du produit
    path('confirmation_commande/<int:commande_id>/', views.confirmation_commande, name='confirmation_commande'),
    path('contactez-nous/', views.contactez_nous, name='contactez_nous'),
    path('conf/', views.conf, name='conf'),
    path('facture/<int:commande_id>/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
  path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
path('panier/', views.gerer_panier, name='gerer_panier'),
    path('commander_panier/', views.commander_panier, name='commander_panier'),
    path('confirmationn_commande/<int:commande_id>/', views.confirmationn_commande, name='confirmationn_commande'),
    path('ajouter-au-panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('admin/dashboard/', dashboard, name='dashboard'),


]
