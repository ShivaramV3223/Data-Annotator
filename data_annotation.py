import streamlit as st
import pandas as pd

# Load CSV data
@st.cache_data
def load_data():
    df = pd.read_csv('cardiac_patients.csv')  # Replace with your file path
    return df

# Main app
st.title("Cardiac Patient Annotation")

data = load_data()

# Function to annotate the row
def annotate_row(patient_id, data, comment, category):
    if "annotations" not in st.session_state:
        st.session_state.annotations = {}
    
    # Save the annotation in session state and CSV file
    st.session_state.annotations[patient_id] = comment
    data.loc[data['Patient ID'] == patient_id, category] = comment
    data = data.set_index("Patient ID")
    data.to_csv('cardiac_patients.csv', index=False)  # Save updates to CSV
    st.session_state[category] = ''  # Clear the text area after submission

# Slider for row navigation
row_idx = st.number_input("Select patient row", min_value=0, max_value=len(data)-1, step=1)
patient_row = data.iloc[row_idx]

# Display the row (excluding the last few columns)
st.subheader(f"Patient ID: {patient_row['Patient ID']}")
st.write(patient_row[data.columns[:-5]])

# Input for annotation - Behavioral Changes
if 'Behavioral Changes' not in st.session_state:
    st.session_state['Behavioral Changes'] = ""

behavior = st.text_area("Behavior Action", value=st.session_state['Behavioral Changes'])
if st.button("Save Behavioral Action"):
    annotate_row(patient_row['Patient ID'], data, behavior, 'Behavioral Changes')

# Input for annotation - Medicinal / Clinical Interventions
if 'Medicinal / Clinical Interventions' not in st.session_state:
    st.session_state['Medicinal / Clinical Interventions'] = ""

medicinal = st.text_area("Medicinal / Clinical Interventions", value=st.session_state['Medicinal / Clinical Interventions'])
if st.button("Save Medicinal Interventions"):
    annotate_row(patient_row['Patient ID'], data, medicinal, 'Medicinal / Clinical Interventions')

# Input for annotation - Lifestyle Changes
if 'Lifestyle Changes' not in st.session_state:
    st.session_state['Lifestyle Changes'] = ""

lifestyle = st.text_area("Lifestyle Changes", value=st.session_state['Lifestyle Changes'])
if st.button("Save Lifestyle Changes"):
    annotate_row(patient_row['Patient ID'], data, lifestyle, 'Lifestyle Changes')

# Input for annotation - Next Visit
if 'Next Visit' not in st.session_state:
    st.session_state['Next Visit'] = ""

next_visit = st.text_area("Next Visit", value=st.session_state['Next Visit'])
if st.button("Save Next Visit"):
    annotate_row(patient_row['Patient ID'],data,  next_visit, 'Next Visit')

# Input for annotation - Diagnostic Test
if 'Diagnostic Test' not in st.session_state:
    st.session_state['Diagnostic Test'] = ""

diag_test = st.text_area("Diagnostic Test", value=st.session_state['Diagnostic Test'])
if st.button("Save Diagnostic Test"):
    annotate_row(patient_row['Patient ID'],data, diag_test, 'Diagnostic Test')

# # Display all annotations (Optional)
# st.sidebar.title("Saved Annotations")
# st.sidebar.write(st.session_state.get("annotations", {}))
