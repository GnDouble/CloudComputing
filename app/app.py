import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
import wikipedia as wp
from datetime import datetime
import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_user(email: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email, hashed_password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"email": row[0], "hashed_password": row[1]}
    return None

def create_user(email: str, password: str):
    conn = sqlite3.connect("users.db")
    hashed_password = pwd_context.hash(password)
    try:
        conn.execute("INSERT INTO users (email, hashed_password) VALUES (?, ?)", (email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'show_login_form' not in st.session_state:
    st.session_state.show_login_form = False
if 'show_register_form' not in st.session_state:
    st.session_state.show_register_form = False

def login(email, password):
    user = get_user(email)
    if user and verify_password(password, user['hashed_password']):
        st.session_state.logged_in = True
        st.session_state.email = email
        st.session_state.show_login_form = False
        st.session_state.show_register_form = False
        st.success("Logged in successfully!")
    else:
        st.error("Invalid email or password")


def register(email, password):
    if create_user(email, password):
        st.session_state.show_register_form = False
        st.success("Registered successfully!")
    else:
        st.error("Email already registered")

def logout():
    st.session_state.logged_in = False
    st.session_state.email = ""
    st.success("Logged out successfully!")

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
    st.session_state.plants = ["empty"] # get Plants from db
if 'medical_history' not in st.session_state:
    st.session_state.medical_history = pd.DataFrame(columns=["Date", "Plant", "Symptoms", "Watering routine", "Treatment"])


if not st.session_state.logged_in:
    col1, col2 = st.columns([9, 4])
    with col2:
        col3,col4 = st.columns([5,5])
        with col3:
            if st.button(":green[Login]"):
                st.session_state.show_login_form = True
                st.session_state.show_register_form = False
        with col4:

            if st.button("Register"):
                st.session_state.show_register_form = True
                st.session_state.show_login_form = False
else:
    col1, col2 = st.columns([9, 4])
    with col2:
        st.write(f"Welcome, {st.session_state.email}")
        if st.button("Logout"):
            logout()

if st.session_state.show_login_form:
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Submit Login"):
        login(email, password)

if st.session_state.show_register_form:
    st.subheader("Register")
    reg_email = st.text_input("Register Email", key="register_email")
    reg_password = st.text_input("Register Password", type="password", key="register_password")
    if st.button("Submit Registration"):
        register(reg_email, reg_password)


# Layout for plant information and query submission
if st.session_state.logged_in:
    col1, col2 = st.columns([4, 2])

    with col1:
        # Step 1: Get crop name
        crop_name = st.text_input(label="Enter the name of the crop:")

        if crop_name:
            # Get plant information from Wikipedia
            plant_info = getPlant(crop_name)
            #st.write("Information about the crop:", plant_info)

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
                        st.write_stream(m.choices[0].delta.content for m in completion if not m.choices[0].finish_reason)
    with col2:
        st.subheader("Plants")
        option = st.selectbox("Your plants:", st.session_state.plants) 
        st.write("You selected:", option)
        
        new_plant = st.text_input("Name of new plant")
        if st.button("Add new plant"):
            if new_plant:
                st.session_state.plants.append(new_plant)
                st.success(f"Pflanze '{new_plant}' hinzugefügt!")

else:
    # Step 1: Get crop name
        crop_name = st.text_input(label="Enter the name of the crop:")

        if crop_name:
            plant_info = getPlant(crop_name)
            #st.write("Information about the crop:", plant_info)

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
                        st.write_stream(m.choices[0].delta.content for m in completion if not m.choices[0].finish_reason)
    
watering_times = ["1","2","2+"]

# Medical history form
st.subheader("Medical History")
with st.form(key='medical_history_form'):
    plant = st.write(f"Plant: :green[{crop_name}]", )
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


