import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
import wikipedia as wp

st.header("leafLover 🌱", divider="green")



#search_item = wp.summary(f"" + query)
#print(search_item)



client = OpenAI(
    base_url="https://chat-large.llm.mylab.th-luebeck.dev/v1",
    api_key="-"
)

completion =""


if 'plants' not in st.session_state:
    st.session_state.plants = ["Email", "Home phone", "Mobile phone"]

with st.container():
    col1, col2, col3 = st.columns([10,2,4])

    with col1:
        query = st.text_area(label="Prompt:")
   
   

    with col2:
        st.write("")
        st.write("")
        st.write("")
        button = st.button(":red[Submit]")
        if button:
            completion = client.chat.completions.create(
        model="tgi",
        messages=[
            {"role": "system", "content": f"Du bist ein Pflanzendoc und ein Pflanzenratgeber, deine Information bekommst du von" },
            {"role": "user", "content": f"{query}\nAntwort:"}
        ],
        stream=True,
        max_tokens=1024
    )

    with col3:
        option = st.selectbox(
            "Deine Pflanzen: ",
            st.session_state.plants
        )
        st.write("Auswahl:", option)
        
        
        new_plant = st.text_input("Your plants")
        if st.button("Add new plant"):
            
            if new_plant:
                st.session_state.plants.append(new_plant)
                st.success(f"Plant '{new_plant}' added!")
    
       
       

# iterate and print stream
    st.write_stream(m.choices[0].delta.content for m in completion if not m.choices[0].finish_reason)






