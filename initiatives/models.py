from django.db import models

# Create your models here.

class Initiative(models.Model):
    from django.db import models

class Initiative(models.Model):
    CATEGORY_CHOICES = [
        ('RE', 'Renewable Energy'),
        ('RC', 'Recycling'),
        ('EC', 'Emission Control'),
        ('WC', 'Water Conservation'),  # New category
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('funded', 'Funded'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    funding_goal = models.DecimalField(max_digits=12, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='initiatives/', blank=True, null=True)  # New field
    
    # Metrics
    carbon_saved = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    energy_saved_generated = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    water_saved = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def check_funding_status(self):
        if self.amount_raised >= self.funding_goal and self.status == 'active':
            self.status = 'funded'
            self.save()
    
class ProgressUpdate(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, related_name='progress_updates')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.initiative.title} - {self.title}"