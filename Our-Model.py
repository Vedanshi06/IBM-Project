import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# Load the trained model and feature names
with open('model_with_features.pkl', 'rb') as file:
    model, feature_names = pickle.load(file)

# Load the data once
data = pd.read_csv('long_data_.csv')

# Get unique states
states = (data['States'].unique())
states.sort()
def getAttributes(state):
    state_index = data[data['States'] == state].index[0]
    state_data = data.iloc[state_index]
    region = state_data['Regions']
    latitude = state_data['latitude']
    longitude = state_data['longitude']
    
    return region, latitude, longitude

# Function to preprocess user inputs
def preprocess_input(state, date_input):
    try:
        region, latitude, longitude = getAttributes(state)

        # Preprocess user input
        try:
            date = datetime.strptime(date_input, "%d-%m-%Y")
        except ValueError:
            st.error("Error: Date format should be DD-MM-YYYY.")
            return None

        year = date.year
        month = date.month
        day = date.day

        # Create a dictionary to store the preprocessed input
        input_data = {
            'Year': [year],
            'Month': [month],
            'Day': [day],
            'States_' + state: [1],
            'Regions_' + region: [1],
            'latitude': [latitude],
            'longitude': [longitude]
        }

        # Create a new data point for prediction
        new_data_point = pd.DataFrame(input_data)

        # Add missing state and region columns with 0 values
        all_states = list(data['States'].unique())
        all_regions = list(data['Regions'].unique())
        for s in all_states:
            if 'States_' + s not in new_data_point.columns:
                new_data_point['States_' + s] = 0
        for r in all_regions:
            if 'Regions_' + r not in new_data_point.columns:
                new_data_point['Regions_' + r] = 0

        # Ensure the new data point has all the required columns in the correct order
        new_data_point = new_data_point.reindex(columns=feature_names, fill_value=0)

        return new_data_point

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit app
st.set_page_config(
    page_title="Quantum Leap IBM project",
    page_icon = "icon.png"
)
st.title('Energy Consumption Prediction')

st.sidebar.success("Above mentioned are the Team Members! Feel free to contact!")

# Input fields
state = st.selectbox('Select State', options=states)  # Replace with actual state options
date_input = st.text_input('Enter Date (DD-MM-YYYY)', '')

# Prediction button
if st.button('Predict'):
    if date_input:
        input_data = preprocess_input(state, date_input)
        if input_data is not None:
            # Debug: Print columns to check
            # st.write("Input data columns:", input_data.columns.tolist())

            prediction = model.predict(input_data)
            st.write(f'Predicted Energy Consumption: {prediction[0]:.3f} mW')
        else:
            st.error("Failed to preprocess input data.")
    else:
        st.error("Please enter a date in the format DD-MM-YYYY.")
