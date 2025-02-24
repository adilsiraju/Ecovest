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