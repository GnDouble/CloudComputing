import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
import wikipedia as wp

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

# Initialize session state for plants if not already set
if 'plants' not in st.session_state:
    st.session_state.plants = ["Email", "Home phone", "Mobile phone"]

with st.container():
    # Step 1: Get crop name
    crop_name = st.text_input(label="Enter the name of the crop:")

    if crop_name:
        # Get plant information from Wikipedia
        plant_info = getPlant(crop_name)
        st.write("Information about the crop:", plant_info)

        # Step 2: Get the problem/query about the crop
        query = st.text_area(label="Describe the problem with the crop:")

        if query:
            button = st.button(":red[Submit]")
            if button:
                completion = client.chat.completions.create(
                    model="tgi",
                    messages=[
                        {"role": "system", "content": f"Du bist ein Pflanzendoc und ein Pflanzenratgeber, deine Information bekommst du von {plant_info}" },
                        {"role": "user", "content": f"{query}\nAntwort:"}
                    ],
                    stream=True,
                    max_tokens=1024
                )
                st.write("Processing your request...")

# Iterate and print stream if completion is available
st.write_stream(m.choices[0].delta.content for m in completion if not m.choices[0].finish_reason)

