import streamlit as st
import openai
from datetime import datetime, date
from gtts import gTTS
import tempfile

# Load API Key securely from Streamlit Cloud Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit Setup 
st.set_page_config(page_title="STAT-TECH-AI - Where Innovation Matters", page_icon="🔮")
st.title("🔮 STAT-TECH-AI: Your Horoscope Pandit") 

st.write("Enter your birth details to get your horoscope:")

# User Inputs
name = st.text_input("Your Name")
dob = st.date_input("Date of Birth", min_value=date(1900, 1, 1), max_value=date.today())
tob = st.text_input("Time of Birth (HH:MM in 24-hour format)", value="12:00")
pob = st.text_input("Place of Birth")

# Horoscope Type Selection
horoscope_type = st.radio(
    "Select Horoscope Type:",
    ("General Horoscope", "Yearly Horoscope", "Monthly Horoscope")
)

# Extra Inputs for Yearly or Monthly Horoscope
if horoscope_type == "Yearly Horoscope":
    target_year = st.number_input("Select Year", min_value=1900, max_value=2100, value=date.today().year)
elif horoscope_type == "Monthly Horoscope":
    target_month = st.selectbox(
        "Select Month",
        ("January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December")
    )
    target_year = st.number_input("Select Year", min_value=1900, max_value=2100, value=date.today().year)

# Output Mode
output_mode = st.selectbox(
    "Choose how you want your horoscope:",
    ("I want to read", "I want to listen", "I want to read and listen")
)

# Generate Horoscope
if st.button("Generate Horoscope"):
    if not name.strip() or not tob.strip() or not pob.strip():
        st.error("⚠️ Please fill all required fields: Name, Time of Birth, Place of Birth.")
    else:
        try:
            dob_str = dob.strftime("%d %B %Y")
            time_obj = datetime.strptime(tob, "%H:%M")
            tob_str = time_obj.strftime("%I:%M %p")

            # Build Prompt
            if horoscope_type == "General Horoscope":
                prompt = (
                    f"Prepare a general personality-based horoscope for:\n"
                    f"Name: {name}\nDate of Birth: {dob_str}\nTime of Birth: {tob_str}\nPlace of Birth: {pob}\n"
                    f"Include strengths, challenges, and life insights."
                )
            elif horoscope_type == "Yearly Horoscope":
                prompt = (
                    f"Prepare a detailed horoscope for {name} for the year {target_year}.\n"
                    f"Date of Birth: {dob_str}\nTime of Birth: {tob_str}\nPlace of Birth: {pob}\n"
                    f"Include predictions for career, relationships, health, and personal growth."
                )
            elif horoscope_type == "Monthly Horoscope":
                prompt = (
                    f"Prepare a detailed horoscope for {name} for the month of {target_month} {target_year}.\n"
                    f"Date of Birth: {dob_str}\nTime of Birth: {tob_str}\nPlace of Birth: {pob}\n"
                    f"Include predictions for career, relationships, health, and personal growth."
                )

            with st.spinner("Consulting the stars..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert astrologer providing horoscopes."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=700
                )

            horoscope = response['choices'][0]['message']['content']

            if output_mode in ["I want to read", "I want to read and listen"]:
                st.success(f"Here's your {horoscope_type}:")
                st.write(horoscope)

            if output_mode in ["I want to listen", "I want to read and listen"]:
                tts = gTTS(horoscope, lang='en')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    audio_bytes = open(fp.name, 'rb').read()

                st.audio(audio_bytes, format='audio/mp3')

        except Exception as e:
            st.error(f"Error: {e}")
