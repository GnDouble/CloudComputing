import streamlit as st
import pandas as pd
from openai import OpenAI
import requests as rq
from bs4 import BeautifulSoup

# Initialize OpenAI client
client = OpenAI(
    base_url="https://chat-mts.models.th-luebeck.dev/v1",
    api_key="-"
)

# Function to get a summarized version of the Wikipedia page
def get_wikipedia_content(page_title, max_paragraphs=6):
    try:
        url = f"https://en.wikipedia.org/wiki/{page_title}"
        response = rq.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser') 
            paragraphs = soup.find_all('p')
            content = "\n".join([para.get_text() for para in paragraphs[:max_paragraphs] if para.get_text().strip()])
            return content
        else:
            return f"Error: Unable to retrieve content (Status code: {response.status_code})"
    except Exception as e:
        return f"An error occurred: {str(e)}"

st.header("leafLover 🌱")

# Initialize session state for medical history and form submission status
if "medical_history" not in st.session_state:
    st.session_state.medical_history = pd.DataFrame(
        columns=["Plant", "Symptoms", "Watering Routine", "Treatment"]
    )

# Initialize session state variables to track form inputs and status
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "plant_info" not in st.session_state:
    st.session_state.plant_info = ""
if "symptoms" not in st.session_state:
    st.session_state.symptoms = ""
if "watering_frequency" not in st.session_state:
    st.session_state.watering_frequency = ""
if "watering_detail" not in st.session_state:
    st.session_state.watering_detail = ""
if "treatment" not in st.session_state:
    st.session_state.treatment = ""
if "current_crop_name" not in st.session_state:
    st.session_state.current_crop_name = ""

# Function to reset the session state for a new process
def reset_process():
    st.session_state.plant_info = ""
    st.session_state.symptoms = ""
    st.session_state.watering_frequency = ""
    st.session_state.watering_detail = ""
    st.session_state.treatment = ""
    st.session_state.form_submitted = False
    st.session_state.current_crop_name = ""

# Plant name input
crop_name = st.text_input(label="Enter the name of the crop:")

# Check if a new crop name has been entered or if the user wants to start a new process
if crop_name != st.session_state.current_crop_name:
    reset_process()
    st.session_state.current_crop_name = crop_name

if crop_name:
    # Get plant information from Wikipedia
    st.session_state.plant_info = get_wikipedia_content(crop_name)

    # Show form only if it has not been submitted yet
    if not st.session_state.form_submitted:
        st.subheader("Medical History")
        with st.form(key="medical_history_form"):
            st.session_state.symptoms = st.text_input("Symptoms")
            st.session_state.watering_frequency = st.selectbox("Watering frequency", ["Daily", "Weekly"])
            st.session_state.watering_detail = st.selectbox("How often?", ["1", "2", "3", ">3"])
            st.session_state.treatment = st.text_input("Treatment")
            submit_button = st.form_submit_button(label="Add Medical History")

            if submit_button:
                new_entry = {
                    "Plant": crop_name,
                    "Symptoms": st.session_state.symptoms,
                    "Watering Routine": f"{st.session_state.watering_detail} times per {st.session_state.watering_frequency}",
                    "Treatment": st.session_state.treatment,
                }
                st.session_state.medical_history = st.session_state.medical_history._append(
                    new_entry, ignore_index=True
                )
                st.success(f"Medical history entry for {crop_name} added!")
                st.session_state.form_submitted = True  # Mark form as submitted

    # Display medical history only after form submission
    if st.session_state.form_submitted:
        st.subheader(f"Medical History for {crop_name}")
        filtered_history = st.session_state.medical_history[
            st.session_state.medical_history["Plant"] == crop_name
        ]
        st.dataframe(filtered_history)

        # Show query section after the medical history form has been submitted
        query = st.text_area(label="Describe the problem with the crop:")

        if query:
            if st.button("Submit Query"):
                with st.spinner("Processing your request..."):
                    completion = client.chat.completions.create(
                        model="tgi",
                        messages=[
                            {"role": "system", "content": f"You are a plant doctor and advisor. Your information is sourced from: {st.session_state.plant_info}."},
                            {"role": "user", "content": f"{query}\nGeneral info: {st.session_state.plant_info}\nSymptoms: {st.session_state.symptoms}\nWatering Routine: {st.session_state.watering_detail} times per {st.session_state.watering_frequency}\nTreatment: {st.session_state.treatment}\nAnswer:"}
                        ],
                        stream=True,
                        max_tokens=2048
                    )
                    st.write_stream(
                        m.choices[0].delta.content for m in completion if not m.choices[0].finish_reason
                    )
                    # After query is done show a button to start a new process
                    if st.button("Start over"):
                        reset_process()










