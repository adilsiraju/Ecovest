from django.core.management.base import BaseCommand
from initiatives.models import Initiative, Category
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate the database with sustainable initiatives across Indian states'

    def handle(self, *args, **options):
        self.stdout.write('Creating sustainable initiatives across Indian states...')

        # Ensure categories exist
        categories_data = [
            ('Renewable Energy', 'Projects focused on clean energy generation'),
            ('Recycling', 'Waste recycling and circular economy initiatives'),
            ('Emission Control', 'Reducing greenhouse gas emissions'),
            ('Water Conservation', 'Water resource management and conservation'),
            ('Reforestation', 'Forest restoration and tree planting'),
            ('Sustainable Agriculture', 'Eco-friendly farming practices'),
            ('Clean Transportation', 'Electric vehicles and sustainable transport'),
            ('Waste Management', 'Solid waste management solutions'),
            ('Green Technology', 'Innovative environmental technologies'),
            ('Ocean Conservation', 'Marine ecosystem protection'),
        ]

        categories = {}
        for name, desc in categories_data:
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            categories[name] = cat

        # Initiative data organized by state
        initiatives_data = [
            # Maharashtra
            {
                'title': 'Mumbai Coastal Solar Farm',
                'description': 'Large-scale solar energy project along Mumbai coastline to provide clean energy to the city.',
                'location': 'Maharashtra',
                'categories': ['Renewable Energy'],
                'technology_type': 'Solar',
                'goal_amount': Decimal('50000000'),
                'risk_level': 'medium',
                'duration_months': 24,
                'min_investment': Decimal('5000'),
                'roi_estimate': Decimal('12.5'),
                'carbon_reduction_per_investment': 150.0,
                'energy_savings_per_investment': 2000.0,
                'project_scale': 4,
            },
            {
                'title': 'Pune Electric Bus Network',
                'description': 'Transition Pune\'s public transport to electric buses reducing urban emissions.',
                'location': 'Maharashtra',
                'categories': ['Clean Transportation', 'Emission Control'],
                'technology_type': 'EV',
                'goal_amount': Decimal('30000000'),
                'risk_level': 'low',
                'duration_months': 18,
                'min_investment': Decimal('10000'),
                'roi_estimate': Decimal('10.0'),
                'carbon_reduction_per_investment': 200.0,
                'energy_savings_per_investment': 1500.0,
                'project_scale': 3,
            },

            # Karnataka
            {
                'title': 'Bangalore Green Building Initiative',
                'description': 'Developing sustainable building standards and retrofitting existing structures in Bangalore.',
                'location': 'Karnataka',
                'categories': ['Green Technology', 'Emission Control'],
                'technology_type': 'AI',
                'goal_amount': Decimal('25000000'),
                'risk_level': 'medium',
                'duration_months': 36,
                'min_investment': Decimal('25000'),
                'roi_estimate': Decimal('15.0'),
                'carbon_reduction_per_investment': 100.0,
                'energy_savings_per_investment': 1200.0,
                'project_scale': 3,
            },
            {
                'title': 'Mysore Organic Farm Collective',
                'description': 'Creating a network of organic farms in Mysore district promoting sustainable agriculture.',
                'location': 'Karnataka',
                'categories': ['Sustainable Agriculture'],
                'technology_type': 'Organic',
                'goal_amount': Decimal('8000000'),
                'risk_level': 'low',
                'duration_months': 24,
                'min_investment': Decimal('5000'),
                'roi_estimate': Decimal('18.0'),
                'carbon_reduction_per_investment': 80.0,
                'water_savings_per_investment': 5000.0,
                'project_scale': 2,
            },

            # Tamil Nadu
            {
                'title': 'Chennai Wind Energy Corridor',
                'description': 'Establishing wind farms along Tamil Nadu coast for renewable energy generation.',
                'location': 'Tamil Nadu',
                'categories': ['Renewable Energy'],
                'technology_type': 'Wind',
                'goal_amount': Decimal('45000000'),
                'risk_level': 'medium',
                'duration_months': 30,
                'min_investment': Decimal('10000'),
                'roi_estimate': Decimal('14.0'),
                'carbon_reduction_per_investment': 180.0,
                'energy_savings_per_investment': 2500.0,
                'project_scale': 4,
            },
            {
                'title': 'Coimbatore Waste-to-Energy Plant',
                'description': 'Converting municipal waste into clean energy in Coimbatore district.',
                'location': 'Tamil Nadu',
                'categories': ['Waste Management', 'Renewable Energy'],
                'technology_type': 'Chemical',
                'goal_amount': Decimal('20000000'),
                'risk_level': 'high',
                'duration_months': 42,
                'min_investment': Decimal('15000'),
                'roi_estimate': Decimal('16.0'),
                'carbon_reduction_per_investment': 120.0,
                'energy_savings_per_investment': 1800.0,
                'project_scale': 3,
            },

            # Gujarat
            {
                'title': 'Gujarat Solar Park Expansion',
                'description': 'Expanding the Charanka Solar Park to become India\'s largest renewable energy hub.',
                'location': 'Gujarat',
                'categories': ['Renewable Energy'],
                'technology_type': 'Solar',
                'goal_amount': Decimal('75000000'),
                'risk_level': 'medium',
                'duration_months': 48,
                'min_investment': Decimal('25000'),
                'roi_estimate': Decimal('13.5'),
                'carbon_reduction_per_investment': 200.0,
                'energy_savings_per_investment': 3000.0,
                'project_scale': 5,
            },
            {
                'title': 'Ahmedabad EV Charging Network',
                'description': 'Building comprehensive electric vehicle charging infrastructure across Ahmedabad.',
                'location': 'Gujarat',
                'categories': ['Clean Transportation'],
                'technology_type': 'EV',
                'goal_amount': Decimal('15000000'),
                'risk_level': 'low',
                'duration_months': 20,
                'min_investment': Decimal('5000'),
                'roi_estimate': Decimal('11.0'),
                'carbon_reduction_per_investment': 150.0,
                'energy_savings_per_investment': 1000.0,
                'project_scale': 3,
            },

            # Rajasthan
            {
                'title': 'Jodhpur Desert Reforestation',
                'description': 'Large-scale desert reforestation project in Jodhpur using drought-resistant species.',
                'location': 'Rajasthan',
                'categories': ['Reforestation', 'Water Conservation'],
                'technology_type': 'Manual',
                'goal_amount': Decimal('12000000'),
                'risk_level': 'medium',
                'duration_months': 60,
                'min_investment': Decimal('2000'),
                'roi_estimate': Decimal('8.0'),
                'carbon_reduction_per_investment': 250.0,
                'water_savings_per_investment': 8000.0,
                'project_scale': 3,
            },
            {
                'title': 'Jaipur Solar Water Heating Initiative',
                'description': 'Installing solar water heating systems in residential and commercial buildings.',
                'location': 'Rajasthan',
                'categories': ['Renewable Energy', 'Water Conservation'],
                'technology_type': 'Solar',
                'goal_amount': Decimal('8000000'),
                'risk_level': 'low',
                'duration_months': 18,
                'min_investment': Decimal('3000'),
                'roi_estimate': Decimal('12.0'),
                'carbon_reduction_per_investment': 90.0,
                'energy_savings_per_investment': 800.0,
                'water_savings_per_investment': 2000.0,
                'project_scale': 2,
            },

            # Kerala
            {
                'title': 'Kochi Mangrove Restoration',
                'description': 'Restoring mangrove ecosystems along Kerala\'s coastline for biodiversity and carbon sequestration.',
                'location': 'Kerala',
                'categories': ['Ocean Conservation', 'Reforestation'],
                'technology_type': 'Manual',
                'goal_amount': Decimal('6000000'),
                'risk_level': 'low',
                'duration_months': 36,
                'min_investment': Decimal('1000'),
                'roi_estimate': Decimal('9.0'),
                'carbon_reduction_per_investment': 300.0,
                'water_savings_per_investment': 10000.0,
                'project_scale': 2,
            },
            {
                'title': 'Thiruvananthapuram Organic Rice Project',
                'description': 'Converting traditional rice farming to organic methods in Thiruvananthapuram district.',
                'location': 'Kerala',
                'categories': ['Sustainable Agriculture'],
                'technology_type': 'Organic',
                'goal_amount': Decimal('5000000'),
                'risk_level': 'low',
                'duration_months': 24,
                'min_investment': Decimal('2000'),
                'roi_estimate': Decimal('14.0'),
                'carbon_reduction_per_investment': 60.0,
                'water_savings_per_investment': 3000.0,
                'project_scale': 2,
            },

            # Uttar Pradesh
            {
                'title': 'Lucknow Waste Recycling Center',
                'description': 'Establishing a modern waste recycling facility to manage Lucknow\'s municipal waste.',
                'location': 'Uttar Pradesh',
                'categories': ['Waste Management', 'Recycling'],
                'technology_type': 'Mechanical',
                'goal_amount': Decimal('18000000'),
                'risk_level': 'medium',
                'duration_months': 30,
                'min_investment': Decimal('5000'),
                'roi_estimate': Decimal('13.0'),
                'carbon_reduction_per_investment': 110.0,
                'energy_savings_per_investment': 600.0,
                'project_scale': 3,
            },
            {
                'title': 'Varanasi Ganges River Cleanup',
                'description': 'Comprehensive river cleanup and water quality improvement project for the Ganges in Varanasi.',
                'location': 'Uttar Pradesh',
                'categories': ['Water Conservation', 'Emission Control'],
                'technology_type': 'Chemical',
                'goal_amount': Decimal('35000000'),
                'risk_level': 'high',
                'duration_months': 48,
                'min_investment': Decimal('10000'),
                'roi_estimate': Decimal('10.0'),
                'carbon_reduction_per_investment': 180.0,
                'water_savings_per_investment': 15000.0,
                'project_scale': 4,
            },

            # West Bengal
            {
                'title': 'Kolkata Solar Rooftop Initiative',
                'description': 'Installing solar panels on rooftops across Kolkata to promote renewable energy adoption.',
                'location': 'West Bengal',
                'categories': ['Renewable Energy'],
                'technology_type': 'Solar',
                'goal_amount': Decimal('22000000'),
                'risk_level': 'low',
                'duration_months': 24,
                'min_investment': Decimal('5000'),
                'roi_estimate': Decimal('15.0'),
                'carbon_reduction_per_investment': 140.0,
                'energy_savings_per_investment': 1800.0,
                'project_scale': 3,
            },
            {
                'title': 'Darjeeling Tea Estate Sustainability',
                'description': 'Implementing sustainable farming practices in Darjeeling tea estates.',
                'location': 'West Bengal',
                'categories': ['Sustainable Agriculture', 'Water Conservation'],
                'technology_type': 'Organic',
                'goal_amount': Decimal('12000000'),
                'risk_level': 'medium',
                'duration_months': 36,
                'min_investment': Decimal('3000'),
                'roi_estimate': Decimal('12.0'),
                'carbon_reduction_per_investment': 70.0,
                'water_savings_per_investment': 4000.0,
                'project_scale': 2,
            },

            # Madhya Pradesh
            {
                'title': 'Bhopal Wind Farm Development',
                'description': 'Developing wind energy infrastructure in Madhya Pradesh\'s wind-rich regions.',
                'location': 'Madhya Pradesh',
                'categories': ['Renewable Energy'],
                'technology_type': 'Wind',
                'goal_amount': Decimal('28000000'),
                'risk_level': 'medium',
                'duration_months': 42,
                'min_investment': Decimal('8000'),
                'roi_estimate': Decimal('13.0'),
                'carbon_reduction_per_investment': 160.0,
                'energy_savings_per_investment': 2200.0,
                'project_scale': 3,
            },
            {
                'title': 'Indore Smart Waste Management',
                'description': 'Implementing AI-powered waste collection and sorting systems in Indore.',
                'location': 'Madhya Pradesh',
                'categories': ['Waste Management', 'Green Technology'],
                'technology_type': 'AI',
                'goal_amount': Decimal('15000000'),
                'risk_level': 'high',
                'duration_months': 28,
                'min_investment': Decimal('10000'),
                'roi_estimate': Decimal('16.0'),
                'carbon_reduction_per_investment': 130.0,
                'energy_savings_per_investment': 900.0,
                'project_scale': 3,
            },

            # Andhra Pradesh
            {
                'title': 'Visakhapatnam Port Green Energy',
                'description': 'Converting Visakhapatnam Port operations to renewable energy sources.',
                'location': 'Andhra Pradesh',
                'categories': ['Renewable Energy', 'Emission Control'],
                'technology_type': 'Solar',
                'goal_amount': Decimal('40000000'),
                'risk_level': 'medium',
                'duration_months': 36,
                'min_investment': Decimal('15000'),
                'roi_estimate': Decimal('14.0'),
                'carbon_reduction_per_investment': 190.0,
                'energy_savings_per_investment': 2800.0,
                'project_scale': 4,
            },
            {
                'title': 'Tirupati Water Conservation Project',
                'description': 'Implementing rainwater harvesting and groundwater recharge in Tirupati region.',
                'location': 'Andhra Pradesh',
                'categories': ['Water Conservation'],
                'technology_type': 'Manual',
                'goal_amount': Decimal('9000000'),
                'risk_level': 'low',
                'duration_months': 24,
                'min_investment': Decimal('2000'),
                'roi_estimate': Decimal('9.0'),
                'carbon_reduction_per_investment': 50.0,
                'water_savings_per_investment': 12000.0,
                'project_scale': 2,
            },

            # Telangana
            {
                'title': 'Hyderabad Smart City EV Infrastructure',
                'description': 'Building comprehensive electric vehicle infrastructure for Hyderabad Smart City.',
                'location': 'Telangana',
                'categories': ['Clean Transportation', 'Green Technology'],
                'technology_type': 'EV',
                'goal_amount': Decimal('25000000'),
                'risk_level': 'low',
                'duration_months': 30,
                'min_investment': Decimal('5000'),
                'roi_estimate': Decimal('12.0'),
                'carbon_reduction_per_investment': 170.0,
                'energy_savings_per_investment': 1300.0,
                'project_scale': 3,
            },
            {
                'title': 'Warangal Solar Irrigation Project',
                'description': 'Installing solar-powered irrigation systems for farmers in Warangal district.',
                'location': 'Telangana',
                'categories': ['Renewable Energy', 'Sustainable Agriculture'],
                'technology_type': 'Solar',
                'goal_amount': Decimal('16000000'),
                'risk_level': 'low',
                'duration_months': 20,
                'min_investment': Decimal('4000'),
                'roi_estimate': Decimal('15.0'),
                'carbon_reduction_per_investment': 120.0,
                'energy_savings_per_investment': 1600.0,
                'water_savings_per_investment': 6000.0,
                'project_scale': 3,
            },

            # Bihar
            {
                'title': 'Patna Biogas Plant Network',
                'description': 'Establishing community biogas plants across Patna for waste-to-energy conversion.',
                'location': 'Bihar',
                'categories': ['Renewable Energy', 'Waste Management'],
                'technology_type': 'Biofuel',
                'goal_amount': Decimal('10000000'),
                'risk_level': 'medium',
                'duration_months': 24,
                'min_investment': Decimal('3000'),
                'roi_estimate': Decimal('14.0'),
                'carbon_reduction_per_investment': 140.0,
                'energy_savings_per_investment': 1200.0,
                'project_scale': 2,
            },
            {
                'title': 'Gaya Sustainable Agriculture Initiative',
                'description': 'Promoting organic farming and water-efficient irrigation in Gaya district.',
                'location': 'Bihar',
                'categories': ['Sustainable Agriculture', 'Water Conservation'],
                'technology_type': 'Organic',
                'goal_amount': Decimal('7000000'),
                'risk_level': 'low',
                'duration_months': 30,
                'min_investment': Decimal('2000'),
                'roi_estimate': Decimal('13.0'),
                'carbon_reduction_per_investment': 65.0,
                'water_savings_per_investment': 8000.0,
                'project_scale': 2,
            },

            # Odisha
            {
                'title': 'Bhubaneswar Solar City Project',
                'description': 'Transforming Bhubaneswar into a solar-powered city with comprehensive renewable infrastructure.',
                'location': 'Odisha',
                'categories': ['Renewable Energy', 'Green Technology'],
                'technology_type': 'Solar',
                'goal_amount': Decimal('35000000'),
                'risk_level': 'medium',
                'duration_months': 48,
                'min_investment': Decimal('10000'),
                'roi_estimate': Decimal('13.5'),
                'carbon_reduction_per_investment': 175.0,
                'energy_savings_per_investment': 2400.0,
                'project_scale': 4,
            },
            {
                'title': 'Puri Beach Cleanup and Restoration',
                'description': 'Comprehensive beach cleanup and coastal ecosystem restoration in Puri.',
                'location': 'Odisha',
                'categories': ['Ocean Conservation', 'Waste Management'],
                'technology_type': 'Manual',
                'goal_amount': Decimal('5000000'),
                'risk_level': 'low',
                'duration_months': 18,
                'min_investment': Decimal('1000'),
                'roi_estimate': Decimal('8.0'),
                'carbon_reduction_per_investment': 200.0,
                'water_savings_per_investment': 15000.0,
                'project_scale': 2,
            },

            # Punjab
            {
                'title': 'Amritsar Green Transportation Hub',
                'description': 'Developing electric public transportation infrastructure in Amritsar.',
                'location': 'Punjab',
                'categories': ['Clean Transportation'],
                'technology_type': 'EV',
                'goal_amount': Decimal('20000000'),
                'risk_level': 'low',
                'duration_months': 24,
                'min_investment': Decimal('5000'),
                'roi_estimate': Decimal('11.5'),
                'carbon_reduction_per_investment': 155.0,
                'energy_savings_per_investment': 1100.0,
                'project_scale': 3,
            },
            {
                'title': 'Ludhiana Industrial Waste Recycling',
                'description': 'Setting up industrial waste recycling facilities in Ludhiana industrial area.',
                'location': 'Punjab',
                'categories': ['Waste Management', 'Recycling'],
                'technology_type': 'Mechanical',
                'goal_amount': Decimal('25000000'),
                'risk_level': 'high',
                'duration_months': 36,
                'min_investment': Decimal('8000'),
                'roi_estimate': Decimal('15.0'),
                'carbon_reduction_per_investment': 135.0,
                'energy_savings_per_investment': 1000.0,
                'project_scale': 3,
            },

            # Haryana
            {
                'title': 'Gurugram Solar Park Initiative',
                'description': 'Developing large-scale solar parks in Gurugram region for clean energy generation.',
                'location': 'Haryana',
                'categories': ['Renewable Energy'],
                'technology_type': 'Solar',
                'goal_amount': Decimal('30000000'),
                'risk_level': 'medium',
                'duration_months': 30,
                'min_investment': Decimal('10000'),
                'roi_estimate': Decimal('14.0'),
                'carbon_reduction_per_investment': 165.0,
                'energy_savings_per_investment': 2300.0,
                'project_scale': 4,
            },
            {
                'title': 'Faridabad Water Treatment Plant',
                'description': 'Building advanced water treatment facilities for industrial wastewater in Faridabad.',
                'location': 'Haryana',
                'categories': ['Water Conservation', 'Emission Control'],
                'technology_type': 'Chemical',
                'goal_amount': Decimal('18000000'),
                'risk_level': 'medium',
                'duration_months': 28,
                'min_investment': Decimal('6000'),
                'roi_estimate': Decimal('12.0'),
                'carbon_reduction_per_investment': 95.0,
                'water_savings_per_investment': 10000.0,
                'project_scale': 3,
            },

            # Delhi (NCR)
            {
                'title': 'Delhi Green Building Retrofit',
                'description': 'Retrofitting government buildings in Delhi with green technology and energy efficiency measures.',
                'location': 'Delhi',
                'categories': ['Green Technology', 'Emission Control'],
                'technology_type': 'AI',
                'goal_amount': Decimal('40000000'),
                'risk_level': 'low',
                'duration_months': 36,
                'min_investment': Decimal('20000'),
                'roi_estimate': Decimal('13.0'),
                'carbon_reduction_per_investment': 145.0,
                'energy_savings_per_investment': 1900.0,
                'project_scale': 4,
            },
            {
                'title': 'Delhi EV Public Transport Network',
                'description': 'Converting Delhi\'s public bus fleet to electric vehicles and establishing charging infrastructure.',
                'location': 'Delhi',
                'categories': ['Clean Transportation'],
                'technology_type': 'EV',
                'goal_amount': Decimal('50000000'),
                'risk_level': 'medium',
                'duration_months': 42,
                'min_investment': Decimal('15000'),
                'roi_estimate': Decimal('11.0'),
                'carbon_reduction_per_investment': 210.0,
                'energy_savings_per_investment': 1600.0,
                'project_scale': 5,
            },
        ]

        # Create initiatives
        created_count = 0
        for initiative_data in initiatives_data:
            # Get categories
            cats = []
            for cat_name in initiative_data.pop('categories'):
                if cat_name in categories:
                    cats.append(categories[cat_name])

            # Create initiative
            initiative, created = Initiative.objects.get_or_create(
                title=initiative_data['title'],
                defaults=initiative_data
            )

            if created:
                initiative.categories.set(cats)
                initiative.status = 'active'
                initiative.save()
                created_count += 1
                self.stdout.write(f'Created: {initiative.title} in {initiative.location}')
            else:
                self.stdout.write(f'Already exists: {initiative.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} new initiatives across Indian states!'
            )
        )