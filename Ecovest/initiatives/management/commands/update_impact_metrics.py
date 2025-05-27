from django.core.management.base import BaseCommand
from initiatives.models import Initiative
from investments.models import Investment
import time

class Command(BaseCommand):
    help = 'Updates all initiatives with fresh impact metrics from the improved ImpactCalculator'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without actually updating the database',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('Running in DRY RUN mode - no changes will be saved'))
        
        initiatives = Initiative.objects.all()
        count = initiatives.count()
        self.stdout.write(f"Updating impact metrics for {count} initiatives...")
        
        for i, initiative in enumerate(initiatives):
            old_metrics = {
                'carbon': initiative.carbon_reduction_per_investment,
                'energy': initiative.energy_savings_per_investment,
                'water': initiative.water_savings_per_investment
            }
            
            # Enable storing of metrics
            if not dry_run:
                initiative._store_metrics = True
            
            # Calculate fresh metrics
            impact = Investment.calculate_impact_for_amount(initiative, 1000)
            
            # If dry run, don't save but show differences
            if dry_run:
                self.stdout.write(f"[{i+1}/{count}] {initiative.title} (ID: {initiative.id}):")
                self.stdout.write(f"  OLD: Carbon: {old_metrics['carbon']:.2f} kg CO₂, Energy: {old_metrics['energy']:.2f} kWh, Water: {old_metrics['water']:.2f} L")
                self.stdout.write(f"  NEW: Carbon: {impact['carbon']:.2f} kg CO₂, Energy: {impact['energy']:.2f} kWh, Water: {impact['water']:.2f} L")
                
                # Show percentage change for each metric
                carbon_change = ((impact['carbon'] - old_metrics['carbon']) / old_metrics['carbon'] * 100) if old_metrics['carbon'] else float('inf')
                energy_change = ((impact['energy'] - old_metrics['energy']) / old_metrics['energy'] * 100) if old_metrics['energy'] else float('inf')
                water_change = ((impact['water'] - old_metrics['water']) / old_metrics['water'] * 100) if old_metrics['water'] else float('inf')
                
                self.stdout.write(f"  CHANGE: Carbon: {carbon_change:+.1f}%, Energy: {energy_change:+.1f}%, Water: {water_change:+.1f}%")
            else:
                self.stdout.write(f"[{i+1}/{count}] Updated '{initiative.title}' with new impact metrics")
            
            # Small delay to see output
            time.sleep(0.1)
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS('Dry run completed. No changes were made.'))
        else:
            self.stdout.write(self.style.SUCCESS('All initiatives updated successfully with fresh impact metrics.'))