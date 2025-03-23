# Generated by Django 5.1.7 on 2025-03-23 02:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0007_company'),
        ('investments', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='initiatives.company'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='initiative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='initiatives.initiative'),
        ),
    ]
