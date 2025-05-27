from django.db.models import Sum
from decimal import Decimal

class PortfolioAnalyzer:
    def __init__(self):
        # Risk weights based on project scale (1-5)
        self.SCALE_WEIGHTS = {
            1: 1,  # Small projects are lower risk
            2: 2,  # Medium projects
            3: 3,  # Large projects
            4: 4,  # Very large projects
            5: 5,  # Enterprise projects are higher risk
        }
        
        # Risk level weights
        self.RISK_LEVEL_WEIGHTS = {
            'low': 1,
            'medium': 3,
            'high': 5,
        }

    def calculate_risk_score(self, initiative):
        # Base score from project scale
        base_score = self.SCALE_WEIGHTS.get(initiative.project_scale, 3)
        
        # Adjust based on risk level
        risk_level_score = self.RISK_LEVEL_WEIGHTS.get(initiative.risk_level, 3)
        
        # Calculate final score (average of both factors)
        final_score = (base_score + risk_level_score) / 2
        
        return final_score

    def get_risk_label(self, score):
        if score <= 2:
            return 'Low Risk'
        elif score <= 4:
            return 'Medium Risk'
        else:
            return 'High Risk'

    def analyze_portfolio(self, investments):
        if not investments:
            return {
                'total_invested': 0,
                'total_impact': {
                    'carbon': 0,
                    'energy': 0,
                    'water': 0
                },
                'risk_score': 0,
                'risk_label': 'Low Risk',
                'diversification_score': 0
            }

        total_invested = sum(inv.amount for inv in investments)
        total_impact = {
            'carbon': sum(inv.amount * inv.initiative.carbon_reduction_per_investment for inv in investments),
            'energy': sum(inv.amount * inv.initiative.energy_savings_per_investment for inv in investments),
            'water': sum(inv.amount * inv.initiative.water_savings_per_investment for inv in investments)
        }

        # Calculate average risk score
        risk_scores = [self.calculate_risk_score(inv.initiative) for inv in investments]
        avg_risk_score = sum(risk_scores) / len(risk_scores)

        # Calculate diversification score (0-100)
        categories = set()
        for inv in investments:
            categories.update(inv.initiative.categories.all())
        diversification_score = min(100, (len(categories) / 5) * 100)  # Assuming 5 is max categories

        return {
            'total_invested': total_invested,
            'total_impact': total_impact,
            'risk_score': avg_risk_score,
            'risk_label': self.get_risk_label(avg_risk_score),
            'diversification_score': diversification_score
        }

    RISK_WEIGHTS = {
        'Solar': 2,
        'Wind': 3,
        'Hydro': 4,
        'Organic': 3,
        'Mechanical': 2,
        'Chemical': 5,
        'Biofuel': 4,
        'EV': 3,
        'Manual': 1,
        'AI': 4
    }
    
    CATEGORY_WEIGHTS = {
        'Renewable Energy': 2,
        'Recycling': 3,
        'Emission Control': 4,
        'Water Conservation': 3,
        'Reforestation': 2,
        'Sustainable Agriculture': 3,
        'Clean Transportation': 4,
        'Waste Management': 3,
        'Green Technology': 5,
        'Ocean Conservation': 4
    }

    def get_diversification_recommendations(self, user):
        user_investments = user.investments.all()
        
        # Calculate current portfolio distribution
        category_distribution = {}
        technology_distribution = {}
        total_invested = user_investments.aggregate(total=Sum('amount'))['total'] or Decimal('0')

        for inv in user_investments:
            amount = inv.amount
            # Calculate category distribution
            for category in inv.initiative.categories.all():
                if category.name not in category_distribution:
                    category_distribution[category.name] = 0
                category_distribution[category.name] += amount

            # Calculate technology distribution (handle missing technology_type)
            tech = getattr(inv.initiative, 'technology_type', 'Manual')
            if tech not in technology_distribution:
                technology_distribution[tech] = 0
            technology_distribution[tech] += amount

        # Convert to percentages
        for cat in category_distribution:
            category_distribution[cat] = (category_distribution[cat] / total_invested * 100)
        for tech in technology_distribution:
            technology_distribution[tech] = (technology_distribution[tech] / total_invested * 100)

        # Generate recommendations
        recommendations = []
        
        # Check category balance
        if category_distribution:
            max_category_pct = max(category_distribution.values())
            if max_category_pct > 40:
                recommendations.append({
                    'type': 'category_diversification',
                    'message': f'Consider diversifying from {max(category_distribution, key=category_distribution.get)}. Current allocation: {max_category_pct:.1f}%',
                    'severity': 'high' if max_category_pct > 60 else 'medium'
                })

        # Check technology balance
        if technology_distribution:
            max_tech_pct = max(technology_distribution.values())
            if max_tech_pct > 50:
                recommendations.append({
                    'type': 'technology_diversification',
                    'message': f'Consider diversifying from {max(technology_distribution, key=technology_distribution.get)} technology. Current allocation: {max_tech_pct:.1f}%',
                    'severity': 'high' if max_tech_pct > 70 else 'medium'
                })

        return {
            'category_distribution': category_distribution,
            'technology_distribution': technology_distribution,
            'recommendations': recommendations
        } 