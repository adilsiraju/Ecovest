import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import os
from django.conf import settings

class ImpactCalculator:
    def __init__(self):
        self.model_carbon = RandomForestRegressor(n_estimators=100, max_depth=5, min_samples_split=5, random_state=42)
        self.model_energy = RandomForestRegressor(n_estimators=100, max_depth=5, min_samples_split=5, random_state=42)
        self.model_water = RandomForestRegressor(n_estimators=100, max_depth=5, min_samples_split=5, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder_location = LabelEncoder()
        self.label_encoder_technology = LabelEncoder()

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

        self.load_or_train_model()

    def load_or_train_model(self):
        try:
            if all(os.path.exists(f) for f in [self.model_file_carbon, self.model_file_energy, self.model_file_water, self.scaler_file]):
                print("Loading pre-trained models and scaler...")
                with open(self.model_file_carbon, 'rb') as f:
                    self.model_carbon = pickle.load(f)
                with open(self.model_file_energy, 'rb') as f:
                    self.model_energy = pickle.load(f)
                with open(self.model_file_water, 'rb') as f:
                    self.model_water = pickle.load(f)
                with open(self.scaler_file, 'rb') as f:
                    self.scaler = pickle.load(f)
                print("Models and scaler loaded successfully.")
            else:
                print("One or more model/scaler files missing. Training new models...")
                self.train_model()
        except Exception as e:
            print(f"Failed to load models or scaler: {e}. Training new models...")
            self.train_model()

    def train_model(self):
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
            'Sustainable Agriculture': {'carbon': 400, 'energy': 50, 'water': 800},  # Adjusted for agriculture
            'Clean Transportation': {'carbon': 800, 'energy': 750, 'water': 20},
            'Waste Management': {'carbon': 500, 'energy': 400, 'water': 150},
            'Green Technology': {'carbon': 400, 'energy': 350, 'water': 250},
            'Ocean Conservation': {'carbon': 250, 'energy': 50, 'water': 2500}
        }

        # Generate dataset
        for cat_idx, category in enumerate(categories):
            for _ in range(num_samples_per_category):
                # Randomly sample features
                scale = np.random.choice(scales)
                duration = np.random.choice(durations)
                investment = np.random.lognormal(mean=11, sigma=1.5)  # ₹1,000 to ₹2,000,000
                location = np.random.choice(locations)
                technology = np.random.choice(technologies)

                # Create feature vector
                category_vector = [1 if i == cat_idx else 0 for i in range(len(categories))]
                location_encoded = self.label_encoder_location.transform([location])[0]
                technology_encoded = self.label_encoder_technology.transform([technology])[0]
                interaction_term = investment * duration

                # Feature vector: [investment, cat1, ..., cat10, duration, scale, location, tech, interaction]
                features = [investment] + category_vector + [duration, scale, location_encoded, technology_encoded]
                X.append(features)

                # Calculate impacts with noise (±10%)
                base = base_impacts[category]
                noise = np.random.uniform(0.9, 1.1)  # ±10%
                carbon = base['carbon'] * scale_factor * duration_factor * noise
                energy = base['energy'] * scale_factor * duration_factor * noise
                water = base['water'] * scale_factor * duration_factor * noise

                # Apply category-specific constraints
                if category in ['Reforestation', 'Ocean Conservation']:
                    energy = 0  # Zero energy impact
                if category == 'Renewable Energy' and technology == 'Wind':
                    water = 0  # Zero water impact for wind
                if category == 'Clean Transportation' and scale < 3:
                    water = 0  # Zero water for small-scale transport

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

        # Train models
        self.model_carbon.fit(X_transformed, y_carbon)
        self.model_energy.fit(X_transformed, y_energy)
        self.model_water.fit(X_transformed, y_water)

        # Print feature importance
        print("Feature importance (carbon model):", self.model_carbon.feature_importances_)
        print("Feature importance (energy model):", self.model_energy.feature_importances_)
        print("Feature importance (water model):", self.model_water.feature_importances_)

        # Save models and scaler
        os.makedirs(os.path.dirname(self.model_file_carbon), exist_ok=True)
        with open(self.model_file_carbon, 'wb') as f:
            pickle.dump(self.model_carbon, f)
        with open(self.model_file_energy, 'wb') as f:
            pickle.dump(self.model_energy, f)
        with open(self.model_file_water, 'wb') as f:
            pickle.dump(self.model_water, f)
        with open(self.scaler_file, 'wb') as f:
            pickle.dump(self.scaler, f)

    def predict_impact(self, investment_amount, category_names, project_duration_months=12, project_scale=1, location='North India', technology_type='Manual'):
        investment_amount = float(investment_amount)
        mapped_location = location if location in self.label_encoder_location.classes_ else 'Uttar Pradesh'
        location_encoded = self.label_encoder_location.transform([mapped_location])[0]
        mapped_tech = technology_type if technology_type in self.label_encoder_technology.classes_ else 'Manual'
        technology_encoded = self.label_encoder_technology.transform([mapped_tech])[0]

        category_vector = [1 if cat in category_names else 0 for cat in self.categories]
        
        primary_category_index = -1
        for i, cat in enumerate(self.categories):
            if cat in category_names:
                primary_category_index = i
                break
                
        print(f"Category names: {category_names}")
        print(f"Category vector: {category_vector}")
        print(f"Selected primary category: {self.categories[primary_category_index] if primary_category_index >= 0 else 'None'}")
        print(f"Primary index: {primary_category_index}")

        if project_duration_months <= 12:
            duration_factor = project_duration_months / 12.0
        else:
            duration_factor = 1.0 + (np.sqrt(project_duration_months / 12.0) - 1.0) * 0.5
        
        scale_factor = 0.3 + 0.7 * (project_scale ** 0.4)
        
        renewable_energy_base = {'carbon': 45, 'energy': 50, 'water': 0}
        emission_control_base = {'carbon': 350, 'energy': 80, 'water': 100}
        water_conservation_base = {'carbon': 80, 'energy': 30, 'water': 1500}
        recycling_base = {'carbon': 200, 'energy': 120, 'water': 200}
        reforestation_base = {'carbon': 500, 'energy': 0, 'water': 1000}
        clean_transportation_base = {'carbon': 300, 'energy': 250, 'water': 0}
        ocean_conservation_base = {'carbon': 150, 'energy': 0, 'water': 1200}
        waste_management_base = {'carbon': 220, 'energy': 180, 'water': 100}
        green_technology_base = {'carbon': 150, 'energy': 220, 'water': 50}

        # Calculate interaction term
        interaction_term = investment_amount * project_duration_months

        # Construct feature vector matching train_model: [investment, cat1, ..., cat10, duration, scale, location, tech, interaction]
        X = np.array([[investment_amount] + category_vector + [project_duration_months, project_scale, location_encoded, technology_encoded, interaction_term]])
        
        # Apply log transformation to investment_amount and interaction_term
        X_transformed = X.copy()
        X_transformed[:, 0] = np.log1p(X[:, 0])  # investment_amount
        X_transformed[:, -1] = np.log1p(X[:, -1])  # interaction_term
        X_transformed = self.scaler.transform(X_transformed)

        if primary_category_index == 4:  # Reforestation
            carbon_reduced = reforestation_base['carbon'] * scale_factor * duration_factor
            energy_saved = 0
            water_conserved = 1000 * scale_factor * duration_factor
            if mapped_location in ["Assam", "Kerala", "Meghalaya", "West Bengal", "Nagaland"]:
                water_conserved *= 1.2
                
        elif primary_category_index == 0:  # Renewable Energy
            tech_multiplier = 1.15 if "Solar" in mapped_tech else (0.9 if "Wind" in mapped_tech else 0.8)
            carbon_reduced = renewable_energy_base['carbon'] * scale_factor * duration_factor * tech_multiplier
            energy_saved = renewable_energy_base['energy'] * scale_factor * duration_factor * tech_multiplier
            water_conserved = 0
            if project_scale >= 5:
                energy_saved *= 1.2
                
        elif primary_category_index == 2:  # Emission Control
            carbon_reduced = emission_control_base['carbon'] * scale_factor * duration_factor
            energy_saved = emission_control_base['energy'] * scale_factor * duration_factor
            water_conserved = emission_control_base['water'] * scale_factor * duration_factor
            if project_scale >= 4:
                carbon_reduced = 1500
            
        elif primary_category_index == 3:  # Water Conservation
            carbon_reduced = water_conservation_base['carbon'] * scale_factor * duration_factor
            energy_saved = water_conservation_base['energy'] * scale_factor * duration_factor
            water_conserved = water_conservation_base['water'] * scale_factor * duration_factor
            if mapped_location in ["Assam", "Kerala", "Meghalaya"]:
                water_conserved *= 1.15
            
        elif primary_category_index == 1:  # Recycling
            carbon_reduced = recycling_base['carbon'] * scale_factor * duration_factor
            energy_saved = recycling_base['energy'] * scale_factor * duration_factor
            water_conserved = recycling_base['water'] * scale_factor * duration_factor
            
        elif primary_category_index == 6:  # Clean Transportation
            carbon_reduced = clean_transportation_base['carbon'] * scale_factor * duration_factor
            energy_saved = clean_transportation_base['energy'] * scale_factor * duration_factor
            water_conserved = 0
            
        elif primary_category_index == 9:  # Ocean Conservation
            carbon_reduced = ocean_conservation_base['carbon'] * scale_factor * duration_factor
            energy_saved = 0
            water_conserved = ocean_conservation_base['water'] * scale_factor * duration_factor
            
        elif primary_category_index == 7:  # Waste Management
            carbon_reduced = waste_management_base['carbon'] * scale_factor * duration_factor
            energy_saved = waste_management_base['energy'] * scale_factor * duration_factor
            water_conserved = waste_management_base['water'] * scale_factor * duration_factor
            
        elif primary_category_index == 8:  # Green Technology
            carbon_reduced = green_technology_base['carbon'] * scale_factor * duration_factor
            energy_saved = green_technology_base['energy'] * scale_factor * duration_factor
            water_conserved = green_technology_base['water'] * scale_factor * duration_factor
            if "AI" in technology_type:
                water_conserved = 0
        else:
            carbon_reduced = max(0, self.model_carbon.predict(X_transformed)[0])
            energy_saved = max(0, self.model_energy.predict(X_transformed)[0])
            water_conserved = max(0, self.model_water.predict(X_transformed)[0])
            print("Using model fallback for predictions")

        if mapped_location in ["Rajasthan", "Gujarat"] and primary_category_index == 0:
            energy_saved *= 1.1
            
        variation_factor = 1.0 + (np.random.random() - 0.5) * 0.1
        carbon_reduced *= variation_factor
        energy_saved *= 1.0 + (np.random.random() - 0.5) * 0.1
        water_conserved *= 1.0 + (np.random.random() - 0.5) * 0.1
        
        if primary_category_index in [5, 9]:  # Sustainable Agriculture or Ocean Conservation
            energy_saved = 0
            
        carbon_reduced = max(0, carbon_reduced)
        energy_saved = max(0, energy_saved)
        water_conserved = max(0, water_conserved)
        
        print(f"Category: {category_names}, Primary Index: {primary_category_index}")
        print(f"Scale Factor: {scale_factor}, Duration Factor: {duration_factor}")
        print(f"Final Impact - Carbon: {carbon_reduced}, Energy: {energy_saved}, Water: {water_conserved}")
        
        return {
            "carbon": round(carbon_reduced, 2),
            "energy": round(energy_saved, 2),
            "water": round(water_conserved, 2)
        }