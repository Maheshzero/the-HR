import streamlit as st

# Page config
st.set_page_config(page_title="Button Example", layout="centered")

# Title
st.title("🖱️ Button Example in Streamlit")

# Input
name = st.text_input("Enter your name:")

# Button
if st.button("Greet Me"):
    if name:
        st.success(f"Hello, {name}! 👋 Welcome to Streamlit!")
    else:
        st.error("Please enter your name before clicking the button.")

# Another button for demonstration
if st.button("Click Me for a Surprise"):
    st.balloons()
    st.info("🎉 Surprise! You're awesome!")

