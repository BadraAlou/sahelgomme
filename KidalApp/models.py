from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='produits/', null=True, blank=True)

    def __str__(self):
        return self.nom


    def __str__(self):
        return self.nom

class Commande(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('1', 'Paiement par carte'),
        ('2', 'Paiement par orange money'),
        ('3', 'Paiement sur place une fois livré'),
    ]

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    quantite = models.PositiveIntegerField(default=1)
    mode_paiement = models.CharField(max_length=255, choices=MODE_PAIEMENT_CHOICES)
    date_commande = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Commande de {self.produit} par {self.utilisateur if self.utilisateur else 'un utilisateur non connecté'}"

    def save(self, *args, **kwargs):
        if self.produit.stock >= self.quantite:
            super().save(*args, **kwargs)
            self.produit.stock -= self.quantite
            self.produit.save()
        else:
            raise ValueError("Le produit est en rupture de stock.")

class CustomUser(AbstractUser):
    adresse = models.CharField(max_length=100, blank=True)

class Message(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.utilisateur.username} envoyé le {self.date_envoi}"


# models.py

from django.db import models
from django.conf import settings

class Panier(models.Model):
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de {self.utilisateur.username}"

    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.total_price()
        return total


class PanierItem(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite} dans le panier de {self.panier.utilisateur.username}"

    def total_price(self):
        return self.produit.prix * self.quantite


class CommanderPanier(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('1', 'Paiement par carte'),
        ('2', 'Paiement par orange money'),
        ('3', 'Paiement sur place une fois livré'),
    ]

    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='commandes')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    mode_paiement = models.CharField(max_length=255, choices=MODE_PAIEMENT_CHOICES)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande pour {self.panier.utilisateur.username} - {self.date_commande}"
