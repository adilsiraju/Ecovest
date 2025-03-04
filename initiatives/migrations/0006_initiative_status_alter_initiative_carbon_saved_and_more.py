# Generated by Django 4.2.19 on 2025-02-23 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0005_progressupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiative',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('funded', 'Funded'), ('completed', 'Completed')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='carbon_saved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='energy_saved_generated',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='water_saved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
