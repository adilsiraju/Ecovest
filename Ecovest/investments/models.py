from django.db import models
from django.conf import settings
from initiatives.models import Initiative
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from investments.impact_calculator import ImpactCalculator

User = get_user_model()

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Impact metrics at the time of investment
    carbon_impact = models.FloatField(default=0)  # CO2 reduction in kg
    energy_impact = models.FloatField(default=0)  # Energy saved in kWh
    water_impact = models.FloatField(default=0)   # Water saved in liters
    
    def __str__(self):
        return f"{self.user.username}'s investment in {self.initiative.title}"
    
    def calculate_impact(self):
        """Centralized impact calculation using AI model"""
        calculator = ImpactCalculator()
        categories = [cat.name for cat in self.initiative.categories.all()]
        
        # Get impact values as a dictionary
        impact = calculator.predict_impact(
            investment_amount=float(self.amount),
            category_names=categories,
            project_duration_months=self.initiative.duration_months,
            project_scale=self.initiative.project_scale,
            location=self.initiative.location,
            technology_type=self.initiative.technology_type
        )
        
        return impact
    
    @staticmethod
    def calculate_impact_for_amount(initiative, amount):
        """Calculate environmental impact for a given investment amount"""
        from .impact_calculator import ImpactCalculator
        
        calculator = ImpactCalculator()
        category_names = [category.name for category in initiative.categories.all()]
        
        # Calculate impact metrics based on initiative details
        impact = calculator.predict_impact(
            investment_amount=amount,
            category_names=category_names,
            project_duration_months=initiative.duration_months,
            project_scale=initiative.project_scale,
            location=initiative.location,
            technology_type=initiative.technology_type
        )
        
        # Only update stored metrics if we're in a "calculate and store" operation mode
        # For normal predictions, we always return the freshly calculated values
        if amount == 1000 and getattr(initiative, '_store_metrics', False):
            initiative.carbon_reduction_per_investment = impact['carbon']
            initiative.energy_savings_per_investment = impact['energy']
            initiative.water_savings_per_investment = impact['water']
            initiative.save()
        
        return impact
    
    def save(self, *args, **kwargs):
        # Calculate impacts using centralized method
        impacts = self.calculate_impact()
        self.carbon_impact = impacts['carbon']
        self.energy_impact = impacts['energy']
        self.water_impact = impacts['water']
        
        # Update initiative amount if new investment
        if not self.pk:
            # Calculate the new total amount after this investment
            new_total_amount = self.initiative.current_amount + self.amount
            self.initiative.current_amount = new_total_amount
            
            # Check if initiative is now fully funded (100% or more)
            if new_total_amount >= self.initiative.goal_amount and self.initiative.status != 'funded':
                self.initiative.status = 'funded'
                
            self.initiative.save()
            
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Update initiative's current amount when investment is deleted
        self.initiative.current_amount -= self.amount
        self.initiative.save()
        super().delete(*args, **kwargs)

class InvestmentGoal(models.Model):
    GOAL_TYPES = [
        ('amount', 'Investment Amount'),
        ('impact', 'Environmental Impact'),
        ('diversity', 'Portfolio Diversity')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investment_goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_carbon = models.FloatField(null=True, blank=True)
    target_energy = models.FloatField(null=True, blank=True)
    target_water = models.FloatField(null=True, blank=True)
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_progress(self):
        if self.goal_type == 'amount':
            current = self.user.investments.aggregate(total=Sum('amount'))['total'] or 0
            return float((current / self.target_amount * 100) if self.target_amount else 0)
        elif self.goal_type == 'impact':
            profile = self.user.profile
            if not profile:
                return 0
            progress = {
                'carbon': float((profile.carbon_reduced / self.target_carbon * 100) if self.target_carbon else 0),
                'energy': float((profile.energy_saved / self.target_energy * 100) if self.target_energy else 0),
                'water': float((profile.water_conserved / self.target_water * 100) if self.target_water else 0)
            }
            return sum(progress.values()) / len(progress)
        elif self.goal_type == 'diversity':
            from investments.portfolio_analyzer import PortfolioAnalyzer
            analyzer = PortfolioAnalyzer()
            analysis = analyzer.get_diversification_recommendations(self.user)
            
            category_dist = analysis['category_distribution']
            tech_dist = analysis['technology_distribution']
            
            if not category_dist or not tech_dist:
                return 0
                
            category_score = 100 - max(category_dist.values()) if category_dist else 0
            tech_score = 100 - max(tech_dist.values()) if tech_dist else 0
            
            return (category_score + tech_score) / 2