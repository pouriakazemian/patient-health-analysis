# =====================================================
# Project: Patient Health & Medication Data Analysis
# Description: This project analyzes patient health data
# and medication data, including missing value handling,
# blood pressure analysis, activity status impact, age
# group analysis, sorting, duplicate removal, and merging
# =====================================================

import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Step 1: Load datasets
# -------------------------
md = pd.read_csv('medication_data.csv')  # Medication data
pa = pd.read_csv('Patient_data.csv')     # Patient health data

# Display first 5 rows
print("Medication data - first 5 rows:")
print(md.head(5))

print("\nPatient data - first 5 rows:")
print(pa.head(5))

# Check shape of dataframes
print("\nShape of medication data:", md.shape)
print("Shape of patient data:", pa.shape)

# Info about data types
print("\nMedication data info:")
print(md.info())

print("\nPatient data info:")
print(pa.info())

# -------------------------
# Step 2: Check and fill missing values
# -------------------------
print("\nMissing values in medication data:")
print(md.isnull().sum())

print("\nMissing values in patient data:")
print(pa.isnull().sum())

# Fill missing Sport_Status with 'Not Specified'
pa['Sport_Status'] = pa['Sport_Status'].fillna('Not Specified')

# Fill missing Blood Pressure values with column mean
pa['Blood_Pressure_Systolic'] = pa['Blood_Pressure_Systolic'].fillna(pa['Blood_Pressure_Systolic'].mean())
pa['Blood_Pressure_Diastolic'] = pa['Blood_Pressure_Diastolic'].fillna(pa['Blood_Pressure_Diastolic'].mean())

print("\nMissing values after filling in patient data:")
print(pa.isnull().sum())

# -------------------------
# Step 3: Blood Pressure Analysis
# -------------------------
mean_systolic = pa['Blood_Pressure_Systolic'].mean()
mean_diastolic = pa['Blood_Pressure_Diastolic'].mean()

print(f"\nAverage Systolic Blood Pressure: {mean_systolic:.2f}")
print(f"Average Diastolic Blood Pressure: {mean_diastolic:.2f}")

# Check Mohammad's high blood pressure incidents
mohammad_data = pa[pa['Name'] == 'Mohammad']
high_bp_count = ((mohammad_data['Blood_Pressure_Systolic'] > 140) |
                 (mohammad_data['Blood_Pressure_Diastolic'] > 90)).sum()
print(f"\nNumber of times Mohammad's blood pressure was above normal: {high_bp_count}")

# Extract patients with high blood pressure
high_bp_patients = pa[(pa['Blood_Pressure_Systolic'] > 140) |
                       (pa['Blood_Pressure_Diastolic'] > 90)]
print("\nPatients with high blood pressure:")
print(high_bp_patients)

# -------------------------
# Step 4: Activity Status Impact
# -------------------------
active_patients = pa[pa['Sport_Status'] == 'Active']
inactive_patients = pa[pa['Sport_Status'] != 'Active']

# Calculate mean BP for active vs inactive patients
active_systolic_mean = active_patients['Blood_Pressure_Systolic'].mean()
active_diastolic_mean = active_patients['Blood_Pressure_Diastolic'].mean()
inactive_systolic_mean = inactive_patients['Blood_Pressure_Systolic'].mean()
inactive_diastolic_mean = inactive_patients['Blood_Pressure_Diastolic'].mean()

print("\nAverage Blood Pressure for Active patients:")
print(f"Systolic: {active_systolic_mean:.2f}, Diastolic: {active_diastolic_mean:.2f}")

print("\nAverage Blood Pressure for Inactive/Not Specified patients:")
print(f"Systolic: {inactive_systolic_mean:.2f}, Diastolic: {inactive_diastolic_mean:.2f}")

# Optional: Bar plot for visualization
bp_data = pd.DataFrame({
    'Group': ['Active', 'Inactive'],
    'Systolic': [active_systolic_mean, inactive_systolic_mean],
    'Diastolic': [active_diastolic_mean, inactive_diastolic_mean]
})

bp_data.plot(x='Group', y=['Systolic', 'Diastolic'], kind='bar', figsize=(8,5),
             title='Average Blood Pressure by Activity Status')
plt.ylabel('Blood Pressure')
plt.show()

# -------------------------
# Step 5: Age Group Analysis
# -------------------------
bins = [17, 30, 40, 50, 120]
labels = ['18-30', '31-40', '41-50', '51+']
pa['Age_Group'] = pd.cut(pa['Age'], bins=bins, labels=labels)

age_group_bp = pa.groupby('Age_Group')[['Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic']].mean()
print("\nAverage Blood Pressure by Age Group:")
print(age_group_bp)

# -------------------------
# Step 6: Sorting and Removing Duplicates
# -------------------------
pa_sorted = pa.sort_values(by='Age', ascending=True)
print("\nData sorted by Age (first 5 rows):")
print(pa_sorted.head(5))

# Check for duplicates in Name and Age
duplicates = pa_sorted.duplicated(subset=['Name', 'Age'], keep=False)
print(f"\nNumber of duplicate rows based on Name and Age: {duplicates.sum()}")

# Remove duplicates, keep first
pa_cleaned = pa_sorted.drop_duplicates(subset=['Name', 'Age'], keep='first')
print("\nData after removing duplicates (first 5 rows):")
print(pa_cleaned.head(5))

print(f"\nNumber of rows before removing duplicates: {pa_sorted.shape[0]}")
print(f"Number of rows after removing duplicates: {pa_cleaned.shape[0]}")

# -------------------------
# Step 8: Merge Patient and Medication Data
# -------------------------
print("\nColumns in Patient data:", pa.columns)
print("Columns in Medication data:", md.columns)

# Merge on Patient_ID
merged_data = pd.merge(pa, md, on='Patient_ID', how='inner')
print("\nMerged data (first 5 rows):")
print(merged_data.head(5))
print("\nShape of merged data:", merged_data.shape)
