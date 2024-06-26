from django.db import models
from django.utils import timezone

class Departement(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nom

class Employe(models.Model):
    matricule = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    date_embauche = models.DateField()
    departement = models.ForeignKey('Departement', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.prenom} {self.nom}'

class Absence(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    raison = models.TextField()
    
    def __str__(self):
        return self.raison

class Paiement(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_paiement = models.DateField()
    salaire = models.DecimalField(max_digits=10, decimal_places=2)

class Conge(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()

    @property
    def option(self):
        if self.date_fin >= timezone.now().date():
            return "toujours en congé"
        else:
            return "n’est plus en congé"

    def __str__(self):
        return f"{self.employe.nom} - {self.option}"

class Voiture(models.Model):
    matricule = models.CharField(max_length=20, unique=True)
    modele = models.CharField(max_length=100)
    annee = models.IntegerField()

    def __str__(self):
        return f"{self.modele} ({self.matricule})"

class Livraison(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(blank=True, null=True)

    @property
    def statut(self):
        if not self.date_fin or self.date_fin >= timezone.now():
            return "Indisponible"
        else:
            return "Disponible"

    def __str__(self):
        return f"Livraison par {self.employe} avec {self.voiture}"

class Projet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return self.nom

class Tache(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=50, choices=[('En cours', 'En cours'), ('Terminé', 'Terminé')])

    def __str__(self):
        return self.nom
