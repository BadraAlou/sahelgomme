# Generated by Django 5.0.2 on 2024-06-23 08:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KidalApp', '0007_remove_panier_utilisateur_delete_lignepanier_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommanderPanier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode_paiement', models.CharField(choices=[('1', 'Paiement par carte'), ('2', 'Paiement par orange money'), ('3', 'Paiement sur place une fois livré')], max_length=255)),
                ('date_commande', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('panier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandes', to='KidalApp.panier')),
            ],
        ),
        migrations.CreateModel(
            name='PanierItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField(default=1)),
                ('panier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='KidalApp.panier')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KidalApp.produit')),
            ],
        ),
    ]
