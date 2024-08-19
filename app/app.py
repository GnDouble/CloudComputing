import streamlit as st
import pandas as pd
from openai import OpenAI
import wikipedia as wp
from datetime import datetime
import sqlite3
from passlib.context import CryptContext

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database initialization
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

# User management functions
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


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""
if "show_login_form" not in st.session_state:
    st.session_state.show_login_form = False
if "show_register_form" not in st.session_state:
    st.session_state.show_register_form = False

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

def login(email, password):
    user = get_user(email)
    if user and verify_password(password, user["hashed_password"]):
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


client = OpenAI(
    base_url="https://chat-large.llm.mylab.th-luebeck.dev/v1",
    api_key="-"
)


if "plants" not in st.session_state:
    st.session_state.plants = ["empty"]  
if "medical_history" not in st.session_state:
    st.session_state.medical_history = pd.DataFrame(columns=["Date", "Plant", "Symptoms", "Watering routine", "Treatment"])


if not st.session_state.logged_in:
    col1, col2 = st.columns([9, 4])
    with col2:
        col3, col4 = st.columns([5, 5])
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


col1, col2 = st.columns([4, 2])

symptoms= ""
watering= ""
treatment= ""

with col1:
    crop_name = st.text_input(label="Enter the name of the crop:")

    if crop_name:
        # Get plant information from Wikipedia
        plant_info = getPlant(crop_name)

        if not st.session_state.form_submitted:  # Only show form if not submitted
            st.subheader("Medical History")
            with st.form(key="medical_history_form"):
                symptoms = st.text_input("Symptoms")
                watering_frequency = st.selectbox("Watering frequency", ["Daily", "Weekly"])
                watering_detail = st.text_input(f"How often?")
                treatment = st.text_input("Treatment")
                submit_button = st.form_submit_button(label="Add")

                if submit_button:
                    new_entry = {
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Plant": crop_name,
                        "Symptoms": symptoms,
                        "Watering routine": f"{watering_detail} times per {watering_frequency.lower()}",
                        "Treatment": treatment,
                    }
                    st.session_state.medical_history = st.session_state.medical_history._append(new_entry, ignore_index=True)
                    st.success(f"Medical history entry for {crop_name} added!")
                    st.session_state.form_submitted = True  # Set form as submitted


        if st.session_state.form_submitted:
            query = st.text_area(label="Describe the problem with the crop:")    

            if query:
                if st.button("Submit"):
                    with st.spinner("Processing your request..."):
                        completion = client.chat.completions.create(
                            model="tgi",
                            messages=[
                                {"role": "system", "content": f"You are a plant doctor and advisor. Your information is sourced from: {plant_info}."},
                                {"role": "user", "content": f"{query}\nSymptoms: {symptoms}\nWatering routine: {watering}\nTreatment: {treatment}\nAnswer:"}
                            ],
                            stream=True,
                            max_tokens=1024
                        )
                        st.write_stream(m.choices[0].delta.content for m in completion if not m.choices[0].finish_reason)

with col2:
    st.subheader("Plants")
    option = st.selectbox("Your plants:", st.session_state.plants)
    st.write("You selected:", option)

    new_plant = st.write(f":green[{crop_name}]")
    if st.button("Add new plant"):
        if st.session_state.logged_in:
            if new_plant:
                st.session_state.plants.append(new_plant)
                st.success(f"Plant {new_plant} added!")
        else:
            st.error("You must be logged in to save plants.")
