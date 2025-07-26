import streamlit as st
import google.generativeai as genai

# Add basic styling
st.markdown("""
<style>
    .main-header {
        color: #ff4b4b;
    }
    .msds-section {
        margin-top: 1em;
        border-left: 3px solid #ffdd00;
        padding-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Configure API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# App title and description
st.markdown("<h1 class='main-header'>Human MSDS Generator</h1>", unsafe_allow_html=True)
st.write("Turn yourself into a humorous Material Safety Data Sheet!")

# Input text area
user_intro = st.text_area("Introduce yourself", 
                          "I'm generally calm but prone to excited outbursts...")

# Function to create prompt for Gemini
def create_prompt(user_intro):
    prompt = f"""
    Create a humorous Material Safety Data Sheet (MSDS) for a person based on this self-introduction:
    
    "{user_intro}"
    
    Format the MSDS with these sections:
    1. IDENTIFICATION (product name, chemical family, recommended use)
    2. HAZARD IDENTIFICATION (signal word, hazard statements, precautionary statements)
    3. FIRST AID MEASURES (for different emotional states)
    4. HANDLING AND STORAGE (how to interact with this person)
    
    Also include NFPA 704 HAZARD RATINGS in text format:
    - Health (1-4 scale)
    - Flammability (1-4 scale)
    - Reactivity (1-4 scale)
    - Special Hazards (any special symbol)
    
    Make it humorous but respectful, treating human traits like chemical properties.
    Use markdown formatting for readability.
    """
    return prompt

# Function to generate MSDS using Gemini
def generate_msds(prompt):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Process button
if st.button("Generate My MSDS"):
    if user_intro:
        with st.spinner("Analyzing your human composition..."):
            prompt = create_prompt(user_intro)
            try:
                msds_content = generate_msds(prompt)
                
                # Display the result
                st.markdown(msds_content)
                
                # Add download button
                st.download_button(
                    "Download My MSDS",
                    msds_content,
                    file_name="my_msds.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("This might be due to an API key issue or network problem.")
    else:
        st.error("Please introduce yourself first!")