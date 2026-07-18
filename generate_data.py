import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_hospital_data(n_patients=1000):
    np.random.seed(42)
    
    diseases = ['Diabetes', 'Hypertension', 'Heart Disease', 'Asthma', 'Obesity', 
                'Cancer', 'Stroke', 'Kidney Disease', 'COPD', 'Arthritis']
    
    age_groups = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    
    risk_factors = ['Smoking', 'Obesity', 'Sedentary Lifestyle', 'Poor Diet', 
                    'Alcohol', 'Stress', 'Genetics', 'None']
    
    departments = ['Cardiology', 'Neurology', 'Oncology', 'Pulmonology', 
                   'Nephrology', 'Orthopedics', 'General']
    
    data = {
        'patient_id': range(1, n_patients + 1),
        'age_group': np.random.choice(age_groups, n_patients, p=[0.1, 0.15, 0.2, 0.25, 0.2, 0.1]),
        'gender': np.random.choice(['Male', 'Female'], n_patients),
        'disease': np.random.choice(diseases, n_patients),
        'risk_factor': np.random.choice(risk_factors, n_patients),
        'department': np.random.choice(departments, n_patients),
        'admission_date': [(datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') 
                          for _ in range(n_patients)],
        'length_of_stay': np.random.exponential(5, n_patients).astype(int) + 1,
        'total_charges': np.random.normal(15000, 5000, n_patients).round(2),
        'readmitted': np.random.choice([0, 1], n_patients, p=[0.85, 0.15]),
        'satisfaction_score': np.random.randint(1, 6, n_patients)
    }
    
    return pd.DataFrame(data)

def generate_monthly_trends():
    months = pd.date_range('2024-01-01', periods=12, freq='ME')
    return pd.DataFrame({
        'month': months.strftime('%Y-%m'),
        'admissions': np.random.poisson(800, 12),
        'average_stay': np.random.normal(5.5, 0.8, 12).round(1),
        'readmission_rate': np.random.normal(0.15, 0.03, 12).round(3),
        'total_charges': np.random.normal(1200000, 150000, 12).round(0)
    })

if __name__ == '__main__':
    patient_data = generate_hospital_data()
    monthly_trends = generate_monthly_trends()
    
    patient_data.to_csv('patient_data.csv', index=False)
    monthly_trends.to_csv('monthly_trends.csv', index=False)
    
    print("Data generated successfully!")
    print(f"Patient records: {len(patient_data)}")
    print(f"Monthly records: {len(monthly_trends)}")
