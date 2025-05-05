# The Sustainable Investing Platform

![image](https://github.com/user-attachments/assets/4476700f-8d9e-4750-9f17-287efabffb51)


Overview
--------

Ecovest is a sustainable investing platform founded in 2025, dedicated to connecting environmentally conscious investors with high-impact, eco-friendly opportunities. It empowers individuals to support a greener future by funding initiatives and startup companies that align with both financial goals and environmental values.

Mission 
-------
*   **Mission**: To make sustainable investing accessible, impactful, and profitable for everyone, proving that financial returns and planetary good can coexist.
    
![image](https://github.com/user-attachments/assets/6b024469-906f-40a9-bb57-3224ecceb921)

Installation
-----------

Follow these steps to set up the Ecovest project locally:

1. **Clone the repository**
   ```
   git clone https://github.com/adilsiraju/Ecovest
   cd Ecovest
   ```

2. **Create a virtual environment**
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```
   python manage.py migrate
   ```

5. **Create a superuser (admin)**
   ```
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

Investment Options
------------------

*   **Initiatives**: Projects focused on sustainability, such as renewable energy, water conservation, and recycling, offering measurable environmental benefits.
    
*   **Startup Companies**: Innovative green technology and sustainability-focused firms, providing investors a chance to back emerging leaders in the eco-space.

![image](https://github.com/user-attachments/assets/de398c85-f9c4-4242-bfa0-a564d8850da9)

Key Features
------------

*   **AI-Powered Impact Prediction**: Utilizes an advanced AI model, trained on real-world data from 2015–2025, to forecast environmental outcomes—carbon reduced (kg CO2), energy saved (kWh), and water conserved (L)—across multiple categories like Renewable Energy and Green Technology.
    
*   **User Experience**: Investors can browse curated opportunities, invest with ease, and monitor portfolio performance and impact through a transparent, intuitive dashboard.
    
![image](https://github.com/user-attachments/assets/86e055c3-dd86-42ac-bf3f-46acca98630e)

Impact Calculator Models
---------------------

The Ecovest platform includes an AI-powered impact calculator that predicts environmental outcomes for investment projects. Here's how to work with these models:

### Generating Impact Prediction Models

1. **Generate new prediction models** with the improved dataset:
   ```
   python investments/generate_models.py
   ```
   This creates pickle files in `investments/models/` directory for carbon reduction, energy savings, and water conservation predictions.

### Retraining Models with New Data

If you need to retrain the models with modified parameters or additional data:

1. **Edit the training data generation parameters** in `investments/generate_models.py`:
   - Adjust `base_impacts` values for different investment categories
   - Modify `num_samples_per_category` to increase/decrease the dataset size
   - Update location or technology factors to fine-tune regional impact differences
   
2. **Retrain with custom parameters**:
   ```
   # Open the generate_models.py file to make changes
   code investments/generate_models.py
   
   # After making changes, run the script
   python investments/generate_models.py
   ```

3. **Monitor the output** to confirm successful model generation:
   - You should see messages like "Training carbon model..." and "Models saved successfully"
   - Check that new files appear in `investments/models/` directory

### Testing the Models

1. **Testing the models** using Jupyter Notebook:
   ```
   pip install jupyter notebook
   jupyter notebook investments/model_testing.ipynb
   ```
   
3. **Working with the model testing notebook**:
   - Run each cell sequentially (Shift+Enter or click the "Run" button)
   - The notebook tests predictions across different investment categories
   - Visualizes impact scaling with investment amounts
   - Tests how location and technology affect predictions
   - Confirms proper functioning of the impact calculator

### Using the Impact Calculator in Code

```python
from investments.impact_calculator import ImpactCalculator

# Create an instance of the calculator
calculator = ImpactCalculator()

# Predict environmental impact
impact = calculator.predict_impact(
    investment_amount=1000000,  # Amount in rupees
    category_names=['Renewable Energy'],  # Project category
    project_duration_months=12,  # Duration in months
    project_scale=3,  # Scale from 1-5
    location='Karnataka',  # Location in India
    technology_type='Solar'  # Technology used
)

# Access the predictions
carbon_reduced = impact['carbon']  # kg CO2
energy_saved = impact['energy']    # kWh
water_conserved = impact['water']  # Liters
```

### Impact Calculator Technical Details

1. **Model Architecture**:
   - Uses three separate Random Forest Regressor models for carbon, energy, and water predictions
   - Each model has 100 estimators with max depth of 5
   - Features include investment amount, category encoding, project duration, scale, location and technology

2. **Training Dataset**:
   - ~150 data points (15 samples per category × 10 categories)
   - Investment amounts use lognormal distribution
   - Categories included: Renewable Energy, Recycling, Emission Control, Water Conservation, Reforestation, 
     Sustainable Agriculture, Clean Transportation, Waste Management, Green Technology, Ocean Conservation

3. **Feature Engineering**:
   - Investment amounts are log-transformed
   - Categories are one-hot encoded
   - Location and technology use label encoding
   - Includes interaction term between investment amount and project duration

Achievements
------------

*   **Development Stage**: As a newly launched startup in 2025, Ecovest is currently in the development phase, building its platform and establishing partnerships to fund its first wave of sustainable initiatives and companies.
    
*   **Future Goals**: Aims to fund over 1,000 projects, attract $50 million in investments, and reduce 100,000+ tons of CO2 within its first five years.
    
