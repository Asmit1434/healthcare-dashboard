import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.makedirs('screenshots', exist_ok=True)

df = pd.read_csv('patient_data.csv')
monthly = pd.read_csv('monthly_trends.csv')

# 1: Dashboard Overview
readmission_pct = df['readmitted'].mean() * 100
fig = go.Figure()
fig.add_trace(go.Indicator(mode='number', value=len(df), title={'text': 'Total Patients'}, domain={'x': [0, 0.25], 'y': [0, 1]}))
fig.add_trace(go.Indicator(mode='number', value=round(df['length_of_stay'].mean(), 1), title={'text': 'Avg Stay (days)'}, domain={'x': [0.25, 0.5], 'y': [0, 1]}))
fig.add_trace(go.Indicator(mode='number', value=readmission_pct, title={'text': 'Readmission %'}, domain={'x': [0.5, 0.75], 'y': [0, 1]}))
fig.add_trace(go.Indicator(mode='number', value=round(df['satisfaction_score'].mean(), 1), title={'text': 'Avg Satisfaction'}, domain={'x': [0.75, 1], 'y': [0, 1]}))
fig.update_layout(title='Healthcare Dashboard - Key Metrics', height=300, template='plotly_dark')
fig.write_image('screenshots/01_dashboard_overview.png', width=1200, height=300)
print('Screenshot 1 done')

# 2: Disease Prevalence
disease_counts = df['disease'].value_counts()
fig2 = px.bar(x=disease_counts.index, y=disease_counts.values, title='Disease Prevalence', labels={'x': 'Disease', 'y': 'Patient Count'}, color=disease_counts.values, color_continuous_scale='viridis')
fig2.update_layout(template='plotly_dark', height=500)
fig2.write_image('screenshots/02_disease_prevalence.png', width=1200, height=500)
print('Screenshot 2 done')

# 3: Age Group Analysis
age_counts = df['age_group'].value_counts().sort_index()
age_stay = df.groupby('age_group')['length_of_stay'].mean()
fig3 = make_subplots(rows=1, cols=2, subplot_titles=('Patient Distribution by Age', 'Avg Hospital Stay by Age'))
fig3.add_trace(go.Bar(x=age_counts.index, y=age_counts.values, name='Patients', marker_color='#58a6ff'), row=1, col=1)
fig3.add_trace(go.Bar(x=age_stay.index, y=age_stay.values, name='Avg Stay', marker_color='#f97316'), row=1, col=2)
fig3.update_layout(title='Age Group Analysis', template='plotly_dark', height=400, showlegend=False)
fig3.write_image('screenshots/03_age_group_analysis.png', width=1200, height=400)
print('Screenshot 3 done')

# 4: Risk Factor Donut
risk_counts = df['risk_factor'].value_counts()
fig4 = px.pie(values=risk_counts.values, names=risk_counts.index, title='Risk Factor Distribution', hole=0.4)
fig4.update_layout(template='plotly_dark', height=500)
fig4.write_image('screenshots/04_risk_factors.png', width=1200, height=500)
print('Screenshot 4 done')

# 5: Correlation Heatmap
df_encoded = df.copy()
df_encoded['age_group'] = df_encoded['age_group'].astype('category').cat.codes
df_encoded['gender'] = df_encoded['gender'].astype('category').cat.codes
df_encoded['disease'] = df_encoded['disease'].astype('category').cat.codes
df_encoded['risk_factor'] = df_encoded['risk_factor'].astype('category').cat.codes
corr = df_encoded[['age_group', 'gender', 'disease', 'risk_factor', 'length_of_stay', 'total_charges', 'readmitted', 'satisfaction_score']].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Correlation Heatmap - Healthcare Data')
plt.tight_layout()
plt.savefig('screenshots/05_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print('Screenshot 5 done')

print('All Healthcare Dashboard screenshots saved!')
