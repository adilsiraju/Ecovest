from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Badge, CustomUser
from investments.models import Investment

@receiver(post_save, sender=Investment)
def check_badges(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.update_stats()  # Update user stats
        
        # Badge 1: First Investment
        if user.total_investments == 1:
            badge, _ = Badge.objects.get_or_create(
                name="First Investment",
                defaults={
                    "description": "Made your first investment!",
                    "criteria": {"total_investments": 1}
                }
            )
            user.badges.add(badge)
        
        # Badge 2: Eco Champion (Invested $500+)
        if user.total_amount_invested >= 500:
            badge, _ = Badge.objects.get_or_create(
                name="Eco Champion",
                defaults={
                    "description": "Invested $500 or more!",
                    "criteria": {"total_amount_invested": 500}
                }
            )
            user.badges.add(badge)

        # Badge 3: Green Pioneer (Invested in 5+ initiatives)
        if user.total_investments >= 5:
            badge, _ = Badge.objects.get_or_create(
                name="Green Pioneer",
                defaults={
                    "description": "Invested in 5 or more initiatives!",
                    "criteria": {"total_investments": 5}
                }
            )
            user.badges.add(badge)
        
        # Badge 4: Carbon Hero (Reduced 1000 kg CO₂e)
        total_carbon = sum(inv.amount * inv.initiative.carbon_saved for inv in user.investment_set.all())
        if total_carbon >= 1000:
            badge, _ = Badge.objects.get_or_create(
                name="Carbon Hero",
                defaults={
                    "description": "Reduced 1000 kg of CO₂e!",
                    "criteria": {"total_carbon": 1000}
                }
            )
            user.badges.add(badge)
        
        # Badge 5: Energy Saver (Saved/Generated 1000 kWh)
        total_energy = sum(inv.amount * inv.initiative.energy_saved_generated for inv in user.investment_set.all())
        if total_energy >= 1000:
            badge, _ = Badge.objects.get_or_create(
                name="Energy Saver",
                defaults={
                    "description": "Saved/Generated 1000 kWh of energy!",
                    "criteria": {"total_energy": 1000}
                }
            )
            user.badges.add(badge)
        
        # Badge 6: Water Guardian (Conserved 10,000 liters)
        total_water = sum(inv.amount * inv.initiative.water_saved for inv in user.investment_set.all())
        if total_water >= 10000:
            badge, _ = Badge.objects.get_or_create(
                name="Water Guardian",
                defaults={
                    "description": "Conserved 10,000 liters of water!",
                    "criteria": {"total_water": 10000}
                }
            )
            user.badges.add(badge)
