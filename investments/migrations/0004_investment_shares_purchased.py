# Generated by Django 5.1.7 on 2025-03-23 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0003_investment_company_alter_investment_initiative'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='shares_purchased',
            field=models.PositiveIntegerField(default=0, help_text='Number of shares bought (for companies)'),
        ),
    ]
