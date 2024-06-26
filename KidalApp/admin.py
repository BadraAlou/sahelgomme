from django.contrib import admin
from .models import Categorie, Produit, Commande, CustomUser, Message, Panier, PanierItem, CommanderPanier
import admin_thumbnails
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

# Customizing admin interface for Commande model
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['produit', 'utilisateur', 'quantite', 'date_commande', 'mode_paiement']
    list_filter = ['date_commande']
    search_fields = ['produit__nom', 'utilisateur__username']

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', )
    search_fields = ['nom']

@admin_thumbnails.thumbnail('image')     
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'stock', 'categorie', 'description', 'image_thumbnail')
    list_filter = ('categorie',)
    search_fields = ['nom']

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('produit', 'utilisateur', 'quantite', 'prix_total', 'date_commande', 'mode_paiement')
    list_filter = ('date_commande',)
    search_fields = ['produit__nom', 'utilisateur__username']

    def prix_total(self, obj):
        return obj.produit.prix * obj.quantite
    prix_total.short_description = 'Prix total'

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    model = CustomUser
    list_display = ('username', 'email', 'adresse', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'adresse')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('contenu', 'utilisateur', 'date_envoi')
    search_fields = ['contenu', 'utilisateur__username']
    list_filter = ('date_envoi',)


from django.urls import path
from django.contrib import admin
from django.shortcuts import redirect

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(lambda request: redirect('dashboard')), name='dashboard'),
        ]
        return custom_urls + urls

admin_site = CustomAdminSite()
admin_site.register(Categorie)
admin_site.register(Produit)
admin_site.register(Commande)
admin_site.register(CustomUser)
admin_site.register(Message)
admin_site.register(Panier)
admin_site.register(PanierItem)
admin_site.register(CommanderPanier)

# Utilisez ce site personnalisé comme site admin principal
admin.site = admin_site
admin.autodiscover()

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("Sahel Gomme Administration")
admin.site.site_title = _("Sahel Gomme Admin")
admin.site.index_title = _("Bienvenue à Sahel Gomme Admin")
