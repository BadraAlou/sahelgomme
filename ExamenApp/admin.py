from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import Departement, Employe, Absence, Paiement, Conge, Projet, Tache, Voiture, Livraison

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    list_filter = ('content_type',)
    search_fields = ('user__username',)
    date_hierarchy = 'action_time'

class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    list_filter = ('nom',)

class EmployeAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'adresse', 'departement', 'date_embauche')
    search_fields = ('matricule', 'nom', 'prenom')
    list_filter = ('departement', 'date_embauche')

class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_debut', 'date_fin', 'raison')
    search_fields = ('employe__nom', 'employe__matricule')
    list_filter = ('date_debut', 'date_fin')

class PaiementAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_paiement', 'salaire')
    search_fields = ('employe__nom', 'employe__matricule', 'salaire')
    list_filter = ('salaire', 'date_paiement')

class CongeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_debut', 'date_fin', 'option')
    search_fields = ('employe__nom', 'employe__matricule')
    list_filter = ('date_debut', 'date_fin')

class ProjetAdmin(admin.ModelAdmin):
    list_display = ('nom', 'departement', 'date_debut', 'date_fin')
    search_fields = ('nom', 'departement__nom')
    list_filter = ('departement', 'date_debut', 'date_fin')

class TacheAdmin(admin.ModelAdmin):
    list_display = ('nom', 'projet', 'employe', 'date_debut', 'date_fin', 'statut')
    search_fields = ('nom', 'projet__nom', 'employe__nom')
    list_filter = ('projet', 'employe', 'statut', 'date_debut', 'date_fin')

class VoitureAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'modele', 'annee')
    search_fields = ('matricule', 'modele')
    list_filter = ('annee',)

class LivraisonAdmin(admin.ModelAdmin):
    list_display = ('employe', 'voiture', 'date_debut', 'date_fin', 'statut')
    search_fields = ('employe__nom', 'employe__matricule', 'voiture__matricule')
    list_filter = ('date_debut', 'date_fin')

admin.site.register(Employe, EmployeAdmin)
admin.site.register(Departement, DepartementAdmin)
admin.site.register(Absence, AbsenceAdmin)
admin.site.register(Paiement, PaiementAdmin)
admin.site.register(Conge, CongeAdmin)
admin.site.register(Projet, ProjetAdmin)
admin.site.register(Tache, TacheAdmin)
admin.site.register(Voiture, VoitureAdmin)
admin.site.register(Livraison, LivraisonAdmin)
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.site_header = 'Gestion Dentreprise'
admin.site.site_title = 'Gestion Dentreprise'
admin.site.index_title = 'Bienvenue à Sahel Gomme Admin'
