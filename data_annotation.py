import streamlit as st
import pandas as pd
from github import Github
import io
import os

# Access the secret from the environment variable
my_secret_key = os.getenv('TOKEN')
print(my_secret_key)
# github initialization

# Replace 'your_token' with your actual personal access token
g = Github(my_secret_key)

# Example: Get user information
repo = g.get_user().get_repo("Data-Annotator")
contents = repo.get_contents('cardiac_patients.csv')

# Load CSV data
@st.cache_data
def load_data():
    csv_content = contents.decoded_content.decode()
    df = pd.read_csv(io.StringIO(csv_content))
    return df

# Main app
st.title("Cardiac Patient Annotation")
if 'row_idx' not in st.session_state:
    st.session_state.row_idx = 0
    
for i in ['behavior', 'medical', 'lifestyle', 'next_visit', 'diag_test']:
    if i  not in st.session_state:
        st.session_state[i] = ''

data = load_data()

# Function to annotate the row
def annotate_row(patient_id, data, annotation):
    print(annotation)
    for category in annotation:
        data.loc[patient_id, category] = annotation[category]
        st.session_state[category] = ''
        
    updated_csv = data.to_csv(index=False)
    
    repo.update_file(contents.path, 'file update', updated_csv, contents.sha)# Save updates to CSV
      # Clear the text area after submission

# Slider for row navigation
row_idx = st.number_input("Select patient row", min_value=0, max_value=len(data)-1, step=1)
patient_row = data.iloc[row_idx]

if row_idx != st.session_state.row_idx:
    for i in ['behavior', 'medical', 'lifestyle', 'next_visit', 'diag_test']:
        st.session_state[i] = ''
    
# Display the row (excluding the last few columns)
st.subheader(f"Patient ID: {patient_row['Patient ID']}")
st.write(patient_row[data.columns[:-5]])

behavior = st.text_area("Add Behavioral Changes", key = 'behavior')
medical = st.text_area("Add Medical / Clinical Intervention", key = 'medical')
lifestyle = st.text_area('Add Lifestyle Changes', key = 'lifestyle')
next_visit = st.text_area("Add Next Visit", key = 'next_visit')
diag_test = st.text_area("Add Diagnostic Test", key = 'diag_test')
# blank = st.text_area("Add blank", value = st.session_state.blank)

annotation = {
    'Behavioral Changes': behavior,
    "Medicinal / Clinical Interventions": medical,
    "Lifestyle Changes" : lifestyle, 
    'Next Visit': next_visit,
    'Diagnostic Test': diag_test
}

if st.button("Save All Annotations"):
    # Update all annotations at once
    annotate_row(row_idx, data, annotation)
    # Show a success message
    st.success(f"Annotations for Patient ID {row_idx} have been saved.")

