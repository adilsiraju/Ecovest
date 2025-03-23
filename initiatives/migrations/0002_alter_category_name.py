# Generated by Django 5.1.7 on 2025-03-22 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Renewable Energy', 'Renewable Energy'), ('Recycling', 'Recycling'), ('Emission Control', 'Emission Control'), ('Water Conservation', 'Water Conservation')], max_length=100),
        ),
    ]
