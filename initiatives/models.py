from django.db import models

# Create your models here.

class Initiative(models.Model):
    CATEGORY_CHOICES = [
        ('RE', 'Renewable Energy'),
        ('RC', 'Recycling'),
        ('EC', 'Emission Control'),
        ('WC', 'Water Conservation'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    funding_goal = models.DecimalField(max_digits=12, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    # Metrics
    carbon_saved = models.DecimalField(
        max_digits=12, decimal_places=5, default=0,
        verbose_name='Carbon Emissions Reduced (CO₂e Saved)'
    )
    energy_saved_generated = models.DecimalField(
        max_digits=12, decimal_places=5, default=0,
        verbose_name='Energy Saved/Generated (kWh)'
    )
    water_saved = models.DecimalField(
        max_digits=12, decimal_places=5, default=0,
        verbose_name='Water Conservation (Liters Saved)'
    )

    def __str__(self):
        return self.title