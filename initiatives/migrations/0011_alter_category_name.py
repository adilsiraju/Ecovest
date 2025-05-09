# Generated by Django 5.1.7 on 2025-03-23 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0010_remove_company_technology_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Renewable Energy', 'Renewable Energy'), ('Recycling', 'Recycling'), ('Emission Control', 'Emission Control'), ('Water Conservation', 'Water Conservation'), ('Reforestation', 'Reforestation'), ('Sustainable Agriculture', 'Sustainable Agriculture'), ('Clean Transportation', 'Clean Transportation'), ('Waste Management', 'Waste Management'), ('Green Technology', 'Green Technology'), ('Ocean Conservation', 'Ocean Conservation')], max_length=100, unique=True),
        ),
    ]
