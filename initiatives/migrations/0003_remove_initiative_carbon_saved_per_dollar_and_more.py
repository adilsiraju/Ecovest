# Generated by Django 4.2.19 on 2025-02-23 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0002_alter_initiative_carbon_saved_per_dollar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='initiative',
            name='carbon_saved_per_dollar',
        ),
        migrations.AddField(
            model_name='initiative',
            name='carbon_saved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Carbon Emissions Reduced (CO₂e Saved)'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='energy_saved_generated',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Energy Saved/Generated (kWh)'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='water_saved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Water Conservation (Liters Saved)'),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='category',
            field=models.CharField(choices=[('RE', 'Renewable Energy'), ('RC', 'Recycling'), ('EC', 'Emission Control'), ('WC', 'Water Conservation')], max_length=2),
        ),
    ]
