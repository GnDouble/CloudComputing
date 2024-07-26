import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
import wikipedia as wp
from datetime import datetime

st.header("leafLover 🌱", divider="green")

# Function to get plant information from Wikipedia
def getPlant(plant):
    try:
        summary = wp.summary(plant)
        return summary
    except Exception as e:
        return "No information found."

# Initialize OpenAI client
client = OpenAI(
    base_url="https://chat-large.llm.mylab.th-luebeck.dev/v1",
    api_key="-"
)

completion = ""

# Initialize session state for plants and medical history if not already set
if 'plants' not in st.session_state:
    st.session_state.plants = ["Email", "Home phone", "Mobile phone"]
if 'medical_history' not in st.session_state:
    st.session_state.medical_history = pd.DataFrame(columns=["Date", "Plant", "Symptoms", "Watering routine", "Treatment"])

# Layout for plant information and query submission
with st.container():
    col1, col2 = st.columns([3, 1])

    with col1:
        # Step 1: Get crop name
        crop_name = st.text_input(label="Enter the name of the crop:")

        if crop_name:
            # Get plant information from Wikipedia
            plant_info = getPlant(crop_name)
            st.write("Information about the crop:", plant_info)

            # Step 2: Get the problem/query about the crop
            query = st.text_area(label="Describe the problem with the crop:")

            if query:
                if st.button("Submit"):
                    with st.spinner("Processing your request..."):
                        completion = client.chat.completions.create(
                            model="tgi",
                            messages=[
                                {"role": "system", "content": f"Du bist ein Pflanzendoc und ein Pflanzenratgeber, deine Information bekommst du von {plant_info}"},
                                {"role": "user", "content": f"{query}\nAntwort:"}
                            ],
                            stream=True,
                            max_tokens=1024
                        )
                        for m in completion:
                            st.write(m.choices[0].delta.content)

    with col2:
        st.subheader("Plants")
        option = st.selectbox("Deine Pflanzen:", st.session_state.plants)
        st.write("You selected:", option)
        
        new_plant = st.text_input("Name der neuen Pflanze")
        if st.button("Neue Pflanze hinzufügen"):
            if new_plant:
                st.session_state.plants.append(new_plant)
                st.success(f"Pflanze '{new_plant}' hinzugefügt!")

watering_times = ["1","2","2+"]

# Medical history form
st.subheader("Medical History")
with st.form(key='medical_history_form'):
    plant = st.selectbox("Plant", st.session_state.plants)
    symptoms = st.text_input("Symptoms")
    watering = st.selectbox("Watering routine", watering_times)
    treatment = st.text_input("Treatment")
    submit_button = st.form_submit_button(label='Add')

    if submit_button:
        new_entry = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Plant": plant,
            "Symptoms": symptoms,
            "Watering routine": watering,
            "Treatment": treatment,
        }
        st.session_state.medical_history = st.session_state.medical_history.add(new_entry)
        st.success(f"Medical history entry for '{plant}' added!")
        # Display medical history
        st.subheader("Medical History")
        st.dataframe(st.session_state.medical_history)


