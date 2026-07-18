import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from generate_data import generate_hospital_data, generate_monthly_trends

st.set_page_config(page_title="Healthcare Analytics Dashboard", layout="wide")

st.title("Healthcare Analytics Dashboard")

@st.cache_data
def load_data():
    patient_df = generate_hospital_data()
    monthly_df = generate_monthly_trends()
    return patient_df, monthly_df

patient_df, monthly_df = load_data()

st.sidebar.header("Filters")
selected_diseases = st.sidebar.multiselect("Select Diseases", 
                                           patient_df['disease'].unique(),
                                           default=patient_df['disease'].unique()[:3])
selected_age_groups = st.sidebar.multiselect("Select Age Groups",
                                            patient_df['age_group'].unique(),
                                            default=patient_df['age_group'].unique())

filtered_df = patient_df[
    (patient_df['disease'].isin(selected_diseases)) &
    (patient_df['age_group'].isin(selected_age_groups))
]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Patients", len(filtered_df))
with col2:
    st.metric("Avg Length of Stay", f"{filtered_df['length_of_stay'].mean():.1f} days")
with col3:
    st.metric("Readmission Rate", f"{filtered_df['readmitted'].mean()*100:.1f}%")
with col4:
    st.metric("Avg Satisfaction", f"{filtered_df['satisfaction_score'].mean():.2f}/5")

st.subheader("Disease Prevalence")
disease_counts = filtered_df['disease'].value_counts().reset_index()
disease_counts.columns = ['Disease', 'Count']
fig_disease = px.bar(disease_counts, x='Disease', y='Count', 
                     title="Patient Count by Disease",
                     color='Count', color_continuous_scale='Blues')
st.plotly_chart(fig_disease, use_container_width=True)

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Age Group Analysis")
    age_analysis = filtered_df.groupby('age_group').agg({
        'patient_id': 'count',
        'length_of_stay': 'mean',
        'satisfaction_score': 'mean'
    }).reset_index()
    age_analysis.columns = ['Age Group', 'Patient Count', 'Avg Stay', 'Avg Satisfaction']
    
    fig_age = make_subplots(rows=1, cols=2, 
                           subplot_titles=('Patient Distribution', 'Avg Stay by Age'))
    fig_age.add_trace(go.Bar(x=age_analysis['Age Group'], y=age_analysis['Patient Count'],
                            name='Patient Count', marker_color='steelblue'), row=1, col=1)
    fig_age.add_trace(go.Bar(x=age_analysis['Age Group'], y=age_analysis['Avg Stay'],
                            name='Avg Stay', marker_color='coral'), row=1, col=2)
    fig_age.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_age, use_container_width=True)

with col_right:
    st.subheader("Risk Factor Distribution")
    risk_counts = filtered_df['risk_factor'].value_counts().reset_index()
    risk_counts.columns = ['Risk Factor', 'Count']
    fig_risk = px.pie(risk_counts, values='Count', names='Risk Factor',
                      title="Risk Factor Distribution",
                      hole=0.3, color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_risk, use_container_width=True)

st.subheader("Hospital Utilization Trends")
fig_trends = make_subplots(rows=2, cols=2,
                          subplot_titles=('Monthly Admissions', 'Average Length of Stay',
                                        'Readmission Rate', 'Total Charges'))

fig_trends.add_trace(go.Scatter(x=monthly_df['month'], y=monthly_df['admissions'],
                               mode='lines+markers', name='Admissions',
                               line=dict(color='steelblue')), row=1, col=1)

fig_trends.add_trace(go.Scatter(x=monthly_df['month'], y=monthly_df['average_stay'],
                               mode='lines+markers', name='Avg Stay',
                               line=dict(color='coral')), row=1, col=2)

fig_trends.add_trace(go.Scatter(x=monthly_df['month'], y=monthly_df['readmission_rate']*100,
                               mode='lines+markers', name='Readmission Rate',
                               line=dict(color='green')), row=2, col=1)

fig_trends.add_trace(go.Scatter(x=monthly_df['month'], y=monthly_df['total_charges']/1000000,
                               mode='lines+markers', name='Total Charges (M)',
                               line=dict(color='purple')), row=2, col=2)

fig_trends.update_layout(height=600, showlegend=False)
st.plotly_chart(fig_trends, use_container_width=True)

st.subheader("Risk Factor Correlation Analysis")
correlation_data = filtered_df.copy()
correlation_data['risk_encoded'] = pd.Categorical(correlation_data['risk_factor']).codes
correlation_data['disease_encoded'] = pd.Categorical(correlation_data['disease']).codes
correlation_data['age_encoded'] = pd.Categorical(correlation_data['age_group']).codes
correlation_data['gender_encoded'] = pd.Categorical(correlation_data['gender']).codes

corr_cols = ['age_encoded', 'risk_encoded', 'disease_encoded', 'gender_encoded',
             'length_of_stay', 'total_charges', 'readmitted', 'satisfaction_score']
corr_matrix = correlation_data[corr_cols].corr()

fig_corr, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax,
            xticklabels=['Age', 'Risk', 'Disease', 'Gender', 'Stay', 'Charges', 'Readmitted', 'Satisfaction'],
            yticklabels=['Age', 'Risk', 'Disease', 'Gender', 'Stay', 'Charges', 'Readmitted', 'Satisfaction'])
plt.title("Correlation Heatmap")
st.pyplot(fig_corr)

col_dept1, col_dept2 = st.columns(2)

with col_dept1:
    st.subheader("Department Utilization")
    dept_analysis = filtered_df.groupby('department').agg({
        'patient_id': 'count',
        'total_charges': 'sum',
        'length_of_stay': 'mean'
    }).reset_index()
    dept_analysis.columns = ['Department', 'Patient Count', 'Total Charges', 'Avg Stay']
    
    fig_dept = px.bar(dept_analysis, x='Department', y='Patient Count',
                     title="Patients by Department", color='Total Charges',
                     color_continuous_scale='Viridis')
    st.plotly_chart(fig_dept, use_container_width=True)

with col_dept2:
    st.subheader("Disease by Age Group")
    disease_age = pd.crosstab(filtered_df['disease'], filtered_df['age_group'])
    fig_heatmap, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(disease_age, annot=True, cmap='YlOrRd', fmt='d', ax=ax)
    plt.title("Disease Distribution by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Disease")
    st.pyplot(fig_heatmap)

st.subheader("Gender Distribution by Disease")
gender_disease = pd.crosstab(filtered_df['disease'], filtered_df['gender'])
fig_gender = px.bar(gender_disease.reset_index().melt(id_vars='disease'),
                    x='disease', y='value', color='gender',
                    title="Disease Distribution by Gender",
                    barmode='group', color_discrete_sequence=['#636EFA', '#EF553B'])
st.plotly_chart(fig_gender, use_container_width=True)

st.subheader("Cost Analysis by Disease")
cost_analysis = filtered_df.groupby('disease').agg({
    'total_charges': ['mean', 'median', 'std'],
    'length_of_stay': 'mean'
}).round(2)
cost_analysis.columns = ['Mean Cost', 'Median Cost', 'Cost Std', 'Avg Stay']
cost_analysis = cost_analysis.reset_index()

fig_cost = px.scatter(cost_analysis, x='Avg Stay', y='Mean Cost',
                     size='Cost Std', color='disease',
                     title="Cost vs Length of Stay by Disease",
                     hover_data=['Median Cost'])
st.plotly_chart(fig_cost, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard analyzes hospital patient data for insights on disease prevalence, "
               "age group analysis, hospital utilization, and risk factor correlations.")
