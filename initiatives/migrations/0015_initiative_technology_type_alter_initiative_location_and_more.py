# Generated by Django 5.1.7 on 2025-03-25 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0014_remove_initiative_technology_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiative',
            name='technology_type',
            field=models.CharField(choices=[('Solar', 'Solar'), ('Wind', 'Wind'), ('Hydro', 'Hydro'), ('Organic', 'Organic'), ('Mechanical', 'Mechanical'), ('Chemical', 'Chemical'), ('Biofuel', 'Biofuel'), ('EV', 'EV'), ('Manual', 'Manual'), ('AI', 'AI')], default='Manual', max_length=20),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('active', 'Active'), ('funded', 'Funded'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='draft', max_length=20),
        ),
    ]
