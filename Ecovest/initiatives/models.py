from datetime import timedelta
from django.db import models
from django.core.validators import MinValueValidator
from investments.portfolio_analyzer import PortfolioAnalyzer

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, choices=[
        ('Renewable Energy', 'Renewable Energy'),
        ('Recycling', 'Recycling'),
        ('Emission Control', 'Emission Control'),
        ('Water Conservation', 'Water Conservation'),
        ('Reforestation', 'Reforestation'),
        ('Sustainable Agriculture', 'Sustainable Agriculture'),
        ('Clean Transportation', 'Clean Transportation'),
        ('Waste Management', 'Waste Management'),
        ('Green Technology', 'Green Technology'),
        ('Ocean Conservation', 'Ocean Conservation'),
    ])
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Initiative(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('funded', 'Funded'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    LOCATION_CHOICES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal')
    ]
    TECHNOLOGY_CHOICES = [
        ('Solar', 'Solar'),
        ('Wind', 'Wind'),
        ('Hydro', 'Hydro'),
        ('Organic', 'Organic'),
        ('Mechanical', 'Mechanical'),
        ('Chemical', 'Chemical'),
        ('Biofuel', 'Biofuel'),
        ('EV', 'EV'),
        ('Manual', 'Manual'),
        ('AI', 'AI')
    ]
    RISK_CHOICES = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk')
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='initiatives')
    image = models.ImageField(upload_to='initiatives/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default='Karnataka')
    technology_type = models.CharField(max_length=20, choices=TECHNOLOGY_CHOICES, default='Manual')
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES, default='medium')
    duration_months = models.IntegerField(default=12)
    min_investment = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    max_investment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    roi_estimate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    carbon_reduction_per_investment = models.FloatField(default=0)
    energy_savings_per_investment = models.FloatField(default=0)
    water_savings_per_investment = models.FloatField(default=0)
    carbon_impact = models.FloatField(default=0)  # CO2 reduction in kg
    energy_impact = models.FloatField(default=0)  # Energy saved in kWh
    water_impact = models.FloatField(default=0)   # Water saved in liters
    project_scale = models.IntegerField(
        choices=[
            (1, 'Small'),
            (2, 'Medium'),
            (3, 'Large'),
            (4, 'Very Large'),
            (5, 'Enterprise')
        ],
        default=3
    )

    def __str__(self):
        return self.title

    def calculate_risk_score(self):
        analyzer = PortfolioAnalyzer()
        return analyzer.calculate_risk_score(self)
    
    def get_risk_label(self):
        analyzer = PortfolioAnalyzer()
        return analyzer.get_risk_label(self.calculate_risk_score())

    def get_progress_percentage(self):
        if self.goal_amount == 0:
            return 0
        return (self.current_amount / self.goal_amount) * 100
    
    @property
    def end_date(self):
        """Calculate the estimated end date based on created_at and duration_months"""
        if not self.created_at or not self.duration_months:
            return None
        return self.created_at + timedelta(days=self.duration_months*30)  # Approximate 30 days

    class Meta:
        ordering = ['-created_at']

# Utility function to get landlocked states
def get_landlocked_states():
    """Return a list of landlocked Indian states that don't have coastlines"""
    return [
        'Rajasthan', 'Madhya Pradesh', 'Chhattisgarh', 'Haryana', 
        'Delhi', 'Uttar Pradesh', 'Bihar', 'Jharkhand', 'Uttarakhand',
        'Himachal Pradesh', 'Assam', 'Meghalaya', 'Nagaland', 'Manipur',
        'Mizoram', 'Sikkim', 'Tripura', 'Arunachal Pradesh', 'Telangana'
    ]