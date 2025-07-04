import streamlit as st
import openai
from datetime import datetime, date
from gtts import gTTS
import tempfile

# Secure API Key from Streamlit Cloud Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Zodiac Sign Logic
def get_zodiac_sign(day, month):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19): return "Aries"
    if (month == 4 and day >= 20) or (month == 5 and day <= 20): return "Taurus"
    if (month == 5 and day >= 21) or (month == 6 and day <= 20): return "Gemini"
    if (month == 6 and day >= 21) or (month == 7 and day <= 22): return "Cancer"
    if (month == 7 and day >= 23) or (month == 8 and day <= 22): return "Leo"
    if (month == 8 and day >= 23) or (month == 9 and day <= 22): return "Virgo"
    if (month == 9 and day >= 23) or (month == 10 and day <= 22): return "Libra"
    if (month == 10 and day >= 23) or (month == 11 and day <= 21): return "Scorpio"
    if (month == 11 and day >= 22) or (month == 12 and day <= 21): return "Sagittarius"
    if (month == 12 and day >= 22) or (month == 1 and day <= 19): return "Capricorn"
    if (month == 1 and day >= 20) or (month == 2 and day <= 18): return "Aquarius"
    if (month == 2 and day >= 19) or (month == 3 and day <= 20): return "Pisces"

# Image Links with PNGs
image_links = {
    "Aries": "https://www.astrology-zodiac-signs.com/images/aries.png",
    "Taurus": "https://www.astrology-zodiac-signs.com/images/taurus.png",
    "Gemini": "https://www.astrology-zodiac-signs.com/images/gemini.png",
    "Cancer": "https://www.astrology-zodiac-signs.com/images/cancer.png",
    "Leo": "https://www.astrology-zodiac-signs.com/images/leo.png",
    "Virgo": "https://www.astrology-zodiac-signs.com/images/virgo.png",
    "Libra": "https://www.astrology-zodiac-signs.com/images/libra.png",
    "Scorpio": "https://www.astrology-zodiac-signs.com/images/scorpio.png",
    "Sagittarius": "https://www.astrology-zodiac-signs.com/images/sagittarius.png",
    "Capricorn": "https://www.astrology-zodiac-signs.com/images/capricorn.png",
    "Aquarius": "https://www.astrology-zodiac-signs.com/images/aquarius.png",
    "Pisces": "https://www.astrology-zodiac-signs.com/images/pisces.png"
}

# Streamlit Setup
st.set_page_config(page_title="STAT-TECH-AI Horoscope", page_icon="🔮")
st.markdown("""
    <h1 style='text-align: center; color: purple;'>🔮 STAT-TECH-AI: Your Horoscope Pandit 🔮</h1>
    <h4 style='text-align: center; color: teal;'>Discover Your Zodiac and Rashi</h4>
""", unsafe_allow_html=True)

# Inputs
name = st.text_input("Your Name")
dob = st.date_input("Date of Birth", min_value=date(1900, 1, 1), max_value=date.today())
tob = st.text_input("Time of Birth (HH:MM in 24-hour format)", value="12:00")
pob = st.text_input("Place of Birth")

horoscope_type = st.radio("Select Horoscope Type:", ("General Horoscope", "Yearly Horoscope", "Monthly Horoscope"))

if horoscope_type == "Yearly Horoscope":
    target_year = st.number_input("Select Year", min_value=1900, max_value=2100, value=date.today().year)
elif horoscope_type == "Monthly Horoscope":
    target_month = st.selectbox("Select Month", ("January", "February", "March", "April", "May", "June",
                                                  "July", "August", "September", "October", "November", "December"))
    target_year = st.number_input("Select Year", min_value=1900, max_value=2100, value=date.today().year)

output_mode = st.selectbox("Choose Output Mode:", ("I want to read", "I want to listen", "I want to read and listen"))

# Horoscope Generation
if st.button("Generate Horoscope"):
    if not name.strip() or not tob.strip() or not pob.strip():
        st.error("⚠️ Please fill all required fields.")
    else:
        try:
            dob_str = dob.strftime("%d %B %Y")
            time_obj = datetime.strptime(tob, "%H:%M")
            tob_str = time_obj.strftime("%I:%M %p")

            # Zodiac Sign
            zodiac_sign = get_zodiac_sign(dob.day, dob.month)
            st.image(image_links[zodiac_sign], caption=f"Your Zodiac Sign: {zodiac_sign}", use_container_width=True)

            # Kundali Sign (Placeholder)
            kundali_sign = "Kanya (Virgo Rashi)"  # Ideally fetched from Astrology API
            st.image("https://www.astrology-zodiac-signs.com/images/virgo.png",
                     caption=f"Your Kundali Sign (Rashi): {kundali_sign}", use_container_width=True)

            # Build Prompt
            if horoscope_type == "General Horoscope":
                prompt = f"Prepare a general horoscope for {name}, born {dob_str} at {tob_str} in {pob}. Include life insights."
            elif horoscope_type == "Yearly Horoscope":
                prompt = f"Prepare a horoscope for {name} for {target_year}, born {dob_str} at {tob_str} in {pob}."
            else:
                prompt = f"Prepare a horoscope for {name} for {target_month} {target_year}, born {dob_str} at {tob_str} in {pob}."

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
                    st.audio(open(fp.name, 'rb').read(), format='audio/mp3')

        except Exception as e:
            st.error(f"Error: {e}")
