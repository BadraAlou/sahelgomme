# Generated by Django 5.0.2 on 2024-06-23 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KidalApp', '0006_panier_lignepanier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='panier',
            name='utilisateur',
        ),
        migrations.DeleteModel(
            name='LignePanier',
        ),
        migrations.DeleteModel(
            name='Panier',
        ),
    ]