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
        y_water = []

        # Base impact values per ₹1,000 (aligned with original dataset)
        base_impacts = {
            'Renewable Energy': {'carbon': 750, 'energy': 1000, 'water': 50},
            'Recycling': {'carbon': 300, 'energy': 100, 'water': 200},
            'Emission Control': {'carbon': 900, 'energy': 150, 'water': 300},
            'Water Conservation': {'carbon': 100, 'energy': 30, 'water': 3000},
            'Reforestation': {'carbon': 950, 'energy': 0, 'water': 500},
            'Sustainable Agriculture': {'carbon': 400, 'energy': 50, 'water': 800},
            'Clean Transportation': {'carbon': 800, 'energy': 750, 'water': 20},
            'Waste Management': {'carbon': 500, 'energy': 400, 'water': 150},
            'Green Technology': {'carbon': 400, 'energy': 350, 'water': 250},
            'Ocean Conservation': {'carbon': 250, 'energy': 50, 'water': 2500}
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
                duration_factor = duration / 12  # normalized to 1 year
                scale_factor = scale
                
                # Apply location-specific adjustments
                location_factor = 1.0
                if location in ['Rajasthan', 'Gujarat'] and category == 'Renewable Energy':
                    location_factor = 1.3  # More sun for solar energy
                elif location in ['Assam', 'Kerala', 'Meghalaya'] and category == 'Water Conservation':
                    location_factor = 0.8  # Less need for water conservation
                
                # Apply technology-specific adjustments
                tech_factor = 1.0
                if tech == 'AI' and category == 'Green Technology':
                    tech_factor = 1.2  # AI is more efficient
                elif tech == 'Solar' and category == 'Renewable Energy':
                    tech_factor = 1.1  # Solar is efficient
                
                # Calculate final impact values with some randomness
                carbon = base_impacts[category]['carbon'] * impact_multiplier * duration_factor * scale_factor * location_factor * tech_factor
                carbon *= 1.0 + (np.random.random() - 0.5) * 0.2  # Add ±10% variation
                
                energy = base_impacts[category]['energy'] * impact_multiplier * duration_factor * scale_factor * location_factor * tech_factor
                energy *= 1.0 + (np.random.random() - 0.5) * 0.2
                
                water = base_impacts[category]['water'] * impact_multiplier * duration_factor * scale_factor * location_factor * tech_factor
                water *= 1.0 + (np.random.random() - 0.5) * 0.2
                
                # Special cases
                if category in ['Sustainable Agriculture', 'Ocean Conservation']:
                    energy = 0
                
                if category == 'Green Technology' and tech == 'AI':
                    water = 0
                
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
