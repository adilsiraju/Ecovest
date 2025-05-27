"""
Script to generate and save pickle models for the impact calculator.
This will create updated models based on the larger, more diverse dataset.
"""
import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from django.conf import settings
import django
import sys

# Set up Django environment
sys.path.append('c:/Users/adila/Documents/Coding/Projects/Personal/Ecovest/Ecovest')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecovest.settings')
django.setup()

class ModelGenerator:
    def __init__(self):
        print("Initializing model generator...")
        self.model_carbon = RandomForestRegressor(n_estimators=100, max_depth=5, min_samples_split=5, random_state=42)
        self.model_energy = RandomForestRegressor(n_estimators=100, max_depth=5, min_samples_split=5, random_state=42)
        self.model_water = RandomForestRegressor(n_estimators=100, max_depth=5, min_samples_split=5, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder_location = LabelEncoder()
        self.label_encoder_technology = LabelEncoder()

        # Create directory if it doesn't exist
        os.makedirs(os.path.join(settings.BASE_DIR, 'investments/models'), exist_ok=True)

        self.model_file_carbon = os.path.join(settings.BASE_DIR, 'investments/models/carbon_model.pkl')
        self.model_file_energy = os.path.join(settings.BASE_DIR, 'investments/models/energy_model.pkl')
        self.model_file_water = os.path.join(settings.BASE_DIR, 'investments/models/water_model.pkl')
        self.scaler_file = os.path.join(settings.BASE_DIR, 'investments/models/scaler.pkl')

        self.categories = [
            'Renewable Energy', 'Recycling', 'Emission Control', 'Water Conservation',
            'Reforestation', 'Sustainable Agriculture', 'Clean Transportation',
            'Waste Management', 'Green Technology', 'Ocean Conservation'
        ]

        self.label_encoder_location.fit([
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
            'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
            'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
        ])
        self.label_encoder_technology.fit(['Solar', 'Wind', 'Hydro', 'Organic', 'Mechanical', 'Chemical', 'Biofuel', 'EV', 'Manual', 'AI'])

    def generate_and_save_models(self):
        print("Generating training dataset...")
        X, y_carbon, y_energy, y_water, X_transformed = self.generate_training_data()
        
        print("Training carbon model...")
        self.model_carbon.fit(X_transformed, y_carbon)
        
        print("Training energy model...")
        self.model_energy.fit(X_transformed, y_energy)
        
        print("Training water model...")
        self.model_water.fit(X_transformed, y_water)
        
        print("Saving models...")
        # Save models
        with open(self.model_file_carbon, 'wb') as f:
            pickle.dump(self.model_carbon, f)
        
        with open(self.model_file_energy, 'wb') as f:
            pickle.dump(self.model_energy, f)
        
        with open(self.model_file_water, 'wb') as f:
            pickle.dump(self.model_water, f)
        
        with open(self.scaler_file, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        print(f"Models saved successfully to {os.path.dirname(self.model_file_carbon)}")

    def generate_training_data(self):
        """Generate an enhanced training dataset with more samples and diversity."""
        # Define parameters for dataset generation
        num_samples_per_category = 15  # 5 scales × 3 durations
        categories = self.categories
        durations = [6, 12, 18, 24, 36]
        scales = [1, 2, 4, 5, 7]
        locations = self.label_encoder_location.classes_
        technologies = self.label_encoder_technology.classes_

        # Initialize arrays
        X = []
        y_carbon = []
        y_energy = []
        y_water = []        # Base impact values per ₹1,000 (realistic values based on environmental research)
        base_impacts = {
            # Based on real-world benchmarks for carbon, energy, and water (kg CO2, kWh, liters)
            'Renewable Energy': {'carbon': 0.9, 'energy': 1.5, 'water': 0.0},  # CO2 per kWh in India × kWh produced
            'Recycling': {'carbon': 0.3, 'energy': 0.25, 'water': 0.2},  # Per kg of material recycled
            'Emission Control': {'carbon': 0.6, 'energy': 0.15, 'water': 0.1},  # Based on industrial efficiency improvements
            'Water Conservation': {'carbon': 0.05, 'energy': 0.02, 'water': 2.0},  # Based on rainwater harvesting and irrigation efficiency
            'Reforestation': {'carbon': 0.022, 'energy': 0.0, 'water': 0.3},  # CO2 per tree × trees planted
            'Sustainable Agriculture': {'carbon': 0.15, 'energy': 0.0, 'water': 0.45},  # Based on reduced fertilizer and better practices
            'Clean Transportation': {'carbon': 0.2, 'energy': 0.3, 'water': 0.0},  # Based on fuel savings and emissions reduction
            'Waste Management': {'carbon': 0.25, 'energy': 0.2, 'water': 0.15},  # Based on landfill methane reduction
            'Green Technology': {'carbon': 0.15, 'energy': 0.25, 'water': 0.05},  # Based on efficiency improvements
            'Ocean Conservation': {'carbon': 0.1, 'energy': 0.0, 'water': 0.5}  # Based on marine ecosystem restoration
        }

        # Generate dataset
        for cat_idx, category in enumerate(categories):
            for _ in range(num_samples_per_category):
                # Sample parameters
                scale = np.random.choice(scales)
                duration = np.random.choice(durations)
                location = np.random.choice(locations)
                
                # Select appropriate technology based on category
                if category == 'Renewable Energy':
                    tech = np.random.choice(['Solar', 'Wind', 'Hydro'])
                elif category in ['Sustainable Agriculture', 'Reforestation']:
                    tech = np.random.choice(['Organic', 'Manual'])
                elif category == 'Green Technology':
                    tech = np.random.choice(['AI', 'Mechanical', 'Solar', 'Wind', 'EV'])
                elif category == 'Clean Transportation':
                    tech = np.random.choice(['EV', 'Biofuel'])
                else:
                    tech = np.random.choice(['Manual', 'Mechanical', 'Chemical'])
                
                # Generate lognormal distribution for investment amounts
                # Different ranges for different categories
                if category in ['Renewable Energy', 'Clean Transportation']:
                    # These tend to be higher cost
                    investment = np.random.lognormal(mean=12, sigma=1)
                elif category in ['Recycling', 'Waste Management', 'Green Technology']:
                    # Medium cost
                    investment = np.random.lognormal(mean=11, sigma=0.8)
                else:
                    # Lower cost
                    investment = np.random.lognormal(mean=10, sigma=1.2)
                
                # Create one-hot encoding for category
                category_encoding = [0] * 10
                category_encoding[cat_idx] = 1
                
                # Create feature vector
                feature_vector = [
                    investment,
                    *category_encoding,
                    duration,
                    scale,
                    self.label_encoder_location.transform([location])[0],
                    self.label_encoder_technology.transform([tech])[0]
                ]
                  # Calculate impact values
                impact_multiplier = investment / 1000  # per ₹1,000
                
                # Annual impact first, then scale by duration
                annual_base = base_impacts[category]
                
                # Scale factor is nonlinear - diminishing returns with scale
                # Based on real-world efficiency curves
                if scale <= 3:
                    scale_factor = scale * 0.9  # Nearly linear at small scales
                else:
                    scale_factor = 3 + (scale - 3) * 0.7  # Diminishing returns at larger scales
                
                # Duration factor based on project lifecycle (non-linear)
                # Projects often have S-curve impact over time
                if duration <= 12:
                    # Ramp-up phase: slower initial impact
                    duration_factor = (duration / 12) * 0.8
                elif duration <= 24:
                    # Peak efficiency phase
                    duration_factor = 0.8 + 0.4 * ((duration - 12) / 12)
                else:
                    # Mature phase with slight diminishing returns
                    duration_factor = 1.2 + 0.2 * ((duration - 24) / 12)                # Apply location-specific adjustments based on real-world data
                location_factor = 1.0
                
                # Solar power potential by region (based on irradiation data)
                if category == 'Renewable Energy' and tech == 'Solar':
                    if location in ['Rajasthan', 'Gujarat', 'Madhya Pradesh']:
                        location_factor = 1.3  # High solar irradiation regions
                    elif location in ['Maharashtra', 'Karnataka', 'Andhra Pradesh', 'Telangana']:
                        location_factor = 1.2  # Good solar regions
                    elif location in ['Assam', 'Meghalaya', 'Mizoram', 'Arunachal Pradesh']:
                        location_factor = 0.8  # Lower solar potential due to cloud cover
                
                # Wind energy potential by region
                elif category == 'Renewable Energy' and tech == 'Wind':
                    if location in ['Tamil Nadu', 'Gujarat', 'Maharashtra', 'Karnataka']:
                        location_factor = 1.4  # High wind potential states
                    elif location in ['Rajasthan', 'Andhra Pradesh', 'Madhya Pradesh']:
                        location_factor = 1.2  # Moderate wind potential
                    elif location in ['Assam', 'Bihar', 'Jharkhand', 'Uttar Pradesh']:
                        location_factor = 0.7  # Low wind potential
                
                # Hydro power potential by region
                elif category == 'Renewable Energy' and tech == 'Hydro':
                    if location in ['Himachal Pradesh', 'Uttarakhand', 'Arunachal Pradesh', 'Sikkim']:
                        location_factor = 1.5  # Himalayan states with high hydro potential
                    elif location in ['Karnataka', 'Kerala', 'Tamil Nadu']:
                        location_factor = 1.2  # Southern states with good hydro potential
                    elif location in ['Rajasthan', 'Gujarat']:
                        location_factor = 0.6  # Arid regions with low hydro potential
                
                # Water conservation potential by rainfall patterns
                elif category == 'Water Conservation':
                    if location in ['Kerala', 'Assam', 'Meghalaya', 'West Bengal']:
                        location_factor = 1.4  # High rainfall regions
                    elif location in ['Rajasthan', 'Gujarat', 'Haryana']:
                        location_factor = 0.9  # While low rainfall areas benefit from conservation, the absolute water saved is less
                
                # Reforestation potential by region
                elif category == 'Reforestation':
                    if location in ['Uttarakhand', 'Himachal Pradesh', 'Sikkim', 'Arunachal Pradesh']:
                        location_factor = 1.3  # Forest-rich states with good growth potential
                    elif location in ['Maharashtra', 'Madhya Pradesh', 'Odisha']:
                        location_factor = 1.1  # Good reforestation potential
                    elif location in ['Rajasthan', 'Gujarat']:
                        location_factor = 0.8  # Arid regions with slower tree growth
                
                # Ocean conservation by coastal status
                elif category == 'Ocean Conservation':
                    if location in ['Tamil Nadu', 'Kerala', 'Gujarat', 'Maharashtra', 'Andhra Pradesh', 'Odisha', 'West Bengal', 'Goa']:
                        location_factor = 1.2  # Coastal states
                    else:
                        location_factor = 0.1  # Minimal impact for inland states                # Apply technology-specific adjustments based on real-world efficiency data
                tech_factor = 1.0
                
                if category == 'Renewable Energy':
                    if tech == 'Solar':
                        tech_factor = 1.0  # Baseline technology for renewable
                    elif tech == 'Wind':
                        tech_factor = 1.2  # Better ROI in optimal locations
                    elif tech == 'Hydro':
                        tech_factor = 1.5  # Higher energy yield but typically requires larger investment
                
                elif category == 'Green Technology':
                    if tech == 'AI':
                        tech_factor = 1.4  # High efficiency through optimization
                    elif tech == 'Solar':
                        tech_factor = 1.1  # Solar-powered green tech
                    elif tech == 'EV':
                        tech_factor = 1.2  # Electric vehicles tech
                    else:
                        tech_factor = 1.0
                
                elif category == 'Clean Transportation':
                    if tech == 'EV':
                        tech_factor = 1.3  # Electric vehicles have higher carbon reduction
                    elif tech == 'Biofuel':
                        tech_factor = 1.1  # Biofuels have moderate reduction
                
                elif category == 'Sustainable Agriculture':
                    if tech == 'Organic':
                        tech_factor = 1.2  # Organic farming has higher water conservation
                    elif tech == 'Manual':
                        tech_factor = 0.9  # Manual techniques have lower impact
                
                # Calculate final impact values with some randomness
                # All impacts are in real-world units: 
                # - Carbon in kg CO2 equivalent
                # - Energy in kWh
                # - Water in liters                # Final impact calculation using improved formula with clear units
                # These calculations now use the annual_base values defined above
                carbon = annual_base['carbon'] * impact_multiplier * duration_factor * scale_factor * location_factor * tech_factor
                carbon *= 1.0 + (np.random.random() - 0.5) * 0.2  # Add ±10% variation
                
                energy = annual_base['energy'] * impact_multiplier * duration_factor * scale_factor * location_factor * tech_factor
                energy *= 1.0 + (np.random.random() - 0.5) * 0.2
                
                water = annual_base['water'] * impact_multiplier * duration_factor * scale_factor * location_factor * tech_factor
                water *= 1.0 + (np.random.random() - 0.5) * 0.2
                
                # Special cases and realistic caps based on real-world data
                # For Sustainable Agriculture - zero energy impact is realistic
                if category in ['Sustainable Agriculture', 'Reforestation', 'Ocean Conservation']:
                    energy = 0
                    
                # Cap Sustainable Agriculture impacts to realistic ranges
                # Based on typical yield improvements and reduced fertilizer use
                if category == 'Sustainable Agriculture':
                    # For ₹1M investment, max realistic impact would be ~1000 kg CO2
                    max_carbon = 1000 * (investment / 1000000)
                    if carbon > max_carbon:
                        carbon = max_carbon
                    
                    # For ₹1M investment, max realistic water savings would be ~2500L
                    max_water = 2500 * (investment / 1000000)
                    if water > max_water:
                        water = max_water
                        
                # Cap Emission Control to realistic ranges based on industrial data
                if category == 'Emission Control':
                    # For ₹1M investment, max realistic carbon reduction would be ~1500 kg CO2
                    max_carbon = 1500 * (investment / 1000000)
                    if carbon > max_carbon:
                        carbon = max_carbon
                
                # Ocean Conservation impact for landlocked states
                if category == 'Ocean Conservation':
                    landlocked_states = ['Rajasthan', 'Madhya Pradesh', 'Chhattisgarh', 'Haryana', 
                                        'Delhi', 'Uttar Pradesh', 'Bihar', 'Jharkhand']
                    if location in landlocked_states:
                        # Education impact only, not direct conservation
                        carbon = carbon * 0.05  
                        water = water * 0.05
                        
                # Reforestation water impact capping based on forest hydrology research
                if category == 'Reforestation':
                    # For ₹1M investment, max realistic water impact would be ~2000L
                    max_water = 2000 * (investment / 1000000)
                    if water > max_water:
                        water = max_water
                        
                # Water Conservation impact capping based on rainwater harvesting efficiency
                if category == 'Water Conservation':
                    # For ₹1M investment, max realistic water savings would be ~3000L
                    max_water = 3000 * (investment / 1000000)
                    if water > max_water:
                        water = max_water
                
                # Green Technology impact adjustments
                if category == 'Green Technology':
                    if tech == 'AI':
                        # AI may have energy benefits but uses water for cooling
                        water = water * 0.5
                
                X.append(feature_vector)
                y_carbon.append(max(0, carbon))
                y_energy.append(max(0, energy))
                y_water.append(max(0, water))

        # Convert to NumPy arrays
        X = np.array(X)
        y_carbon = np.array(y_carbon)
        y_energy = np.array(y_energy)
        y_water = np.array(y_water)

        # Add interaction term as the last feature
        interaction_term = X[:, 0] * X[:, 11]  # investment_amount * project_duration_months
        X = np.hstack((X, interaction_term.reshape(-1, 1)))

        # Normalize investment amounts and interaction term
        X[:, 0] = np.log1p(X[:, 0])  # investment_amount
        X[:, -1] = np.log1p(X[:, -1])  # interaction_term

        # Fit scaler and transform features
        self.scaler.fit(X)
        X_transformed = self.scaler.transform(X)
        
        return X, y_carbon, y_energy, y_water, X_transformed

if __name__ == "__main__":
    generator = ModelGenerator()
    generator.generate_and_save_models()
    print("Done!")
