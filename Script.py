import os
import openai
import streamlit as st
from openai import OpenAI

# Load environment variables from 'nano.env'
openai = OpenAI()
openai.api_key = st.secrets["OPENAI_API_KEY"]


# Define system prompts and message functions
system_prompt = ("You are an excellent teacher, and you are known for explaining any topic in a very simple way that can be understood easily by a class 8–9 student. Your way of explaining is very appreciated.You first give an introduction to the given topic in 2–3 lines in very simple words, then you give 3–5 most important points related to the topic. The number of points depends on how important/vast is the given topic.Then you finish your explanation by giving a very simple example of 2–3 lines only. Also, you reply everything in Markdown form so that student can read it easily.But you are also a responsible teacher , if a student asks you to explain sensitive topics like 'Sex' , 'Drugs' , 'terrorism' , 'porn' , 'kissing' , etc , you have to resond with something like 'Instead of this , Use this platform to learn something good and useful' , but you also have to be smart enough , like if a student asks to explain topics like 'Reproduction in animals' , 'Good vs bad drugs' , etc you have to explain it. If a student didn't get your explanation,you also have the ability to explain the same topic in a very simple way, i.e., more simpler than original, still maintaining the structure of giving answer."
)

def user_prompt_for(topic):
    return f"Hello teacher, can you please explain the topic: {topic}"

def message_for(topic):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(topic)}
    ]

def conf_message_negative(main_explanation, topic):
    user_prompt2 = (
        f"You just provided me with the following explanation of the topic '{topic}', but I quite didn't get it.Explain it in a more simpler way but maintain the structure of giving the answer:\n"
    )
    user_prompt2 += main_explanation
    return user_prompt2

def message_for_clearing(main_explanation, topic):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": conf_message_negative(main_explanation, topic)}
    ]

# Function to explain the topic using OpenAI API
def explain_topic(topic):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Change to your desired model
        messages=message_for(topic)
    )
    main_explanation = response.choices[0].message.content
    return main_explanation

# Function to clarify explanation if needed
def clarify_explanation(main_explanation, topic):
    response2 = openai.chat.completions.create(
        model="gpt-4o-mini",  # Change to your desired model
        messages=message_for_clearing(main_explanation, topic)
    )
    easier_explanation = response2.choices[0].message.content
    return easier_explanation

# Streamlit App Interface
st.title("Tuition-Topic Explainer")
st.write("Enter a topic below, and get a simple, structured explanation!")
st.write("Note : Do not use it for Homework !!")

# Input from user
topic = st.text_input("Enter a topic:")

if topic:
    # Display the initial explanation
    st.write("Generating explanation...")
    main_explanation = explain_topic(topic)
    st.markdown(main_explanation)

    # Feedback from user
    feedback = st.radio("Did you understand the explanation?", ("Yes", "No"))
    if feedback == "No":
        st.write("Let me try to simplify it further...")
        easier_explanation = clarify_explanation(main_explanation, topic)
        st.markdown(easier_explanation)
    elif feedback == "Yes":
        st.success(f"Glad I was able to explain the topic of '{topic}' to you!")
