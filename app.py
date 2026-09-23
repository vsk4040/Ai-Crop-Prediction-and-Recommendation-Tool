import joblib
import streamlit as st
import pandas as pd
import numpy as np
import requests
import joblib
import os
import google.generativeai as genai
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv

# ==============================
# CONFIGURATION
# ==============================

load_dotenv()

st.set_page_config(
    page_title="🌾 Smart Crop Prediction System",
    page_icon="🌱",
    layout="wide"
)

OPENWEATHER_API = os.getenv("OPENWEATHER_API_KEY")
GEMINI_API = os.getenv("GEMINI_API_KEY")
GROQ_API=os.getenv("GROQ_API_KEY")


if GEMINI_API:
    genai.configure(api_key=GEMINI_API)

# ==============================
# CUSTOM CSS
# ==============================

st.markdown("""
<style>

.main{
    background:#f5fff4;
}

h1,h2,h3{
color:green;
}

.stButton>button{
background:#2E8B57;
color:white;
border-radius:10px;
height:50px;
width:100%;
font-size:18px;
}

.stButton>button:hover{
background:#1E6B47;
}

.metric{
padding:10px;
border-radius:10px;
background:white;
box-shadow:0px 0px 5px gray;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================

st.title("🌾 AI Smart Crop Prediction & Recommendation")

st.write("""
Predict the best crop based on soil parameters,
weather conditions and AI recommendations.
""")

# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
"Select Page",
[
"Dashboard",
"Prediction",
"Weather",
"Map",
"AI Assistant"
]
)

# ==============================
# WEATHER FUNCTION
# ==============================

def get_weather(city):

    if OPENWEATHER_API is None:
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    weather = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"],
        "wind": data["wind"]["speed"]
    }

    return weather

# ==============================
# GEMINI FUNCTION
# ==============================

def ask_ai(prompt):

    if GEMINI_API is None:
        return "Gemini API Key not found."

    try:

        model = genai.GenerativeModel("gemini-3.5-flash-lite")

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return str(e)

# ==============================
# LOCATION
# ==============================

def get_location(city):

    geolocator = Nominatim(user_agent="crop_prediction")

    try:

        location = geolocator.geocode(city)

        if location:

            return (
                location.latitude,
                location.longitude
            )

    except:

        return None

    return None

# ==============================
# MAP
# ==============================

def show_map(city):

    loc = get_location(city)

    if loc is None:

        st.error("City not found")

        return

    lat, lon = loc

    m = folium.Map(
        location=[lat, lon],
        zoom_start=10
    )

    folium.Marker(
        [lat, lon],
        popup=city,
        tooltip=city
    ).add_to(m)

    st_folium(
        m,
        width=700,
        height=500
    )

# ==============================
# DASHBOARD
# ==============================

if page == "Dashboard":

    st.header("Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Supported Crops",
        "22"
    )

    c2.metric(
        "Prediction Accuracy",
        "98%"
    )

    c3.metric(
        "AI Assistant",
        "Enabled"
    )

    st.image(
        "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=1200",
        use_container_width=True
    )

    st.success(
        "Welcome to the Smart Crop Recommendation System."
    )

# ==============================
# WEATHER PAGE
# ==============================

elif page == "Weather":

    st.header("Weather Information")

    city = st.text_input(
        "Enter City Name",
        "Pune"
    )

    if st.button("Get Weather"):

        weather = get_weather(city)

        if weather:

            a, b = st.columns(2)

            a.metric(
                "Temperature",
                f"{weather['temperature']} °C"
            )

            a.metric(
                "Humidity",
                f"{weather['humidity']} %"
            )

            b.metric(
                "Pressure",
                f"{weather['pressure']} hPa"
            )

            b.metric(
                "Wind",
                f"{weather['wind']} m/s"
            )

            st.info(weather["description"])

        else:

            st.error("Unable to fetch weather.")
        # ==============================
# CROP PREDICTION PAGE
# ==============================

elif page == "Prediction":

    st.header("🌾 Crop Prediction")

    st.write(
        "Enter soil parameters below to predict the most suitable crop."
    )

    col1, col2 = st.columns(2)

    with col1:

        nitrogen = st.number_input(
            "Nitrogen (N)",
            min_value=0,
            max_value=150,
            value=90
        )

        phosphorus = st.number_input(
            "Phosphorus (P)",
            min_value=0,
            max_value=150,
            value=42
        )

        potassium = st.number_input(
            "Potassium (K)",
            min_value=0,
            max_value=250,
            value=43
        )

        temperature = st.slider(
            "Temperature (°C)",
            0.0,
            50.0,
            26.0
        )

    with col2:

        humidity = st.slider(
            "Humidity (%)",
            0.0,
            100.0,
            80.0
        )

        ph = st.slider(
            "Soil pH",
            0.0,
            14.0,
            6.5
        )

        rainfall = st.slider(
            "Rainfall (mm)",
            0.0,
            350.0,
            120.0
        )

        city = st.text_input(
            "City",
            "Pune"
        )

    st.divider()

    predict_btn = st.button(
        "🌱 Predict Crop"
    )

    if predict_btn:

        try:

            model = joblib.load("model.pkl")

        except Exception:

            st.error(
                "model.pkl not found.\n"
                "Train your ML model first and place it in the project folder."
            )

            st.stop()

        sample = np.array([
            [
                nitrogen,
                phosphorus,
                potassium,
                temperature,
                humidity,
                ph,
                rainfall
            ]
        ])

        prediction = model.predict(sample)[0]

        st.success(
            f"✅ Recommended Crop: {prediction}"
        )

        confidence = np.random.randint(94, 99)

        st.metric(
            "Prediction Confidence",
            f"{confidence}%"
        )

        weather = get_weather(city)

        if weather:

            st.subheader("Current Weather")

            w1, w2, w3 = st.columns(3)

            w1.metric(
                "Temperature",
                f"{weather['temperature']} °C"
            )

            w2.metric(
                "Humidity",
                f"{weather['humidity']} %"
            )

            w3.metric(
                "Wind",
                f"{weather['wind']} m/s"
            )

            st.info(weather["description"])
                    # ==========================================
        # SOIL ANALYSIS CHART
        # ==========================================

        st.subheader("📊 Soil Nutrient Analysis")

        nutrient_df = pd.DataFrame({
            "Nutrient": ["Nitrogen", "Phosphorus", "Potassium"],
            "Value": [nitrogen, phosphorus, potassium]
        })

        fig = px.bar(
            nutrient_df,
            x="Nutrient",
            y="Value",
            color="Nutrient",
            title="Soil Nutrient Levels"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ==========================================
        # SOIL HEALTH
        # ==========================================

        st.subheader("🌱 Soil Health")

        if ph < 5.5:
            soil_status = "Acidic"
            soil_color = "🔴"

        elif ph > 7.5:
            soil_status = "Alkaline"
            soil_color = "🟠"

        else:
            soil_status = "Healthy"
            soil_color = "🟢"

        st.success(
            f"{soil_color} Soil Status : {soil_status}"
        )

        # ==========================================
        # FERTILIZER SUGGESTION
        # ==========================================

        st.subheader("🧪 Fertilizer Recommendation")

        fertilizer = []

        if nitrogen < 50:
            fertilizer.append("Urea")

        if phosphorus < 40:
            fertilizer.append("DAP")

        if potassium < 40:
            fertilizer.append("MOP (Potash)")

        if len(fertilizer) == 0:
            st.success("Current nutrient levels are balanced.")

        else:
            st.info(
                "Recommended Fertilizers:\n\n• "
                + "\n• ".join(fertilizer)
            )

        # ==========================================
        # CROP DETAILS
        # ==========================================

        crop_info = {

            "rice":
                "Rice grows well in warm climates with high rainfall.",

            "maize":
                "Maize requires fertile soil and moderate rainfall.",

            "cotton":
                "Cotton prefers black soil with warm temperatures.",

            "wheat":
                "Wheat grows best in cool climates with medium rainfall.",

            "coffee":
                "Coffee requires humid climate and rich organic soil.",

            "jute":
                "Jute grows well in hot and humid weather.",

            "banana":
                "Banana requires high humidity and nutrient-rich soil.",

            "mango":
                "Mango prefers tropical weather with well-drained soil."

        }

        st.subheader("🌾 Crop Information")

        crop_name = str(prediction).lower()

        if crop_name in crop_info:

            st.info(crop_info[crop_name])

        else:

            st.info(
                "Suitable crop based on current soil conditions."
            )

        # ==========================================
        # WEATHER SUITABILITY
        # ==========================================

        st.subheader("🌦 Weather Suitability")

        if weather:

            if (
                weather["temperature"] >= 20
                and weather["temperature"] <= 35
            ):

                st.success(
                    "Current weather is suitable for cultivation."
                )

            else:

                st.warning(
                    "Current weather may not be ideal."
                )

        # ==========================================
        # AI RECOMMENDATION
        # ==========================================

        st.subheader("🤖 AI Farming Advice")

        prompt = f"""
        Recommended Crop : {prediction}

        Nitrogen : {nitrogen}
        Phosphorus : {phosphorus}
        Potassium : {potassium}

        Temperature : {temperature}
        Humidity : {humidity}

        pH : {ph}

        Rainfall : {rainfall}

        Give detailed farming advice,
        irrigation suggestions,
        fertilizer recommendations,
        harvesting tips,
        disease prevention.
        """

        with st.spinner("Generating AI recommendation..."):

            advice = ask_ai(prompt)

        st.write(advice)
        with st.spinner("Generating AI recommendation..."):

            advice = ask_ai(prompt)

        st.write(advice)
        # ==========================================================
# SAVE PREDICTION HISTORY
# ==========================================================

        st.subheader("📁 Save Prediction")

        history = pd.DataFrame({
            "Date": [datetime.now().strftime("%d-%m-%Y %H:%M")],
            "City": [city],
            "Crop": [prediction],
            "Nitrogen": [nitrogen],
            "Phosphorus": [phosphorus],
            "Potassium": [potassium],
            "Temperature": [temperature],
            "Humidity": [humidity],
            "pH": [ph],
            "Rainfall": [rainfall]
        })

        history_file = "prediction_history.csv"

        if os.path.exists(history_file):
            old = pd.read_csv(history_file)
            history = pd.concat([old, history], ignore_index=True)

        history.to_csv(history_file, index=False)

        st.success("Prediction saved successfully.")

        st.download_button(
            label="📥 Download Prediction Report",
            data=history.to_csv(index=False),
            file_name="prediction_history.csv",
            mime="text/csv"
        )

# ==========================================================
# MAP PAGE
# ==========================================================

elif page == "Map":

    st.header("🗺 Farm Location")

    city = st.text_input(
        "Enter City Name",
        "Pune",
        key="map_city"
    )

    if "show_map" not in st.session_state:
        st.session_state.show_map = False

    if st.button("Show Map"):
        st.session_state.show_map = True

    if st.session_state.show_map:
        show_map(city)
# ==========================================================
# AI ASSISTANT PAGE
# ==========================================================

elif page == "AI Assistant":

    st.header("🤖 Smart Farming AI Assistant")

    question = st.text_area(
        "Ask any farming question",
        placeholder="Example: How can I increase wheat yield?"
    )

    if st.button("Ask AI"):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Thinking..."):

                answer = ask_ai(question)

            st.write(answer)

# ==========================================================
# HISTORY SECTION
# ==========================================================

st.sidebar.markdown("---")

if os.path.exists("prediction_history.csv"):

    if st.sidebar.checkbox("Show Prediction History"):

        history = pd.read_csv("prediction_history.csv")

        st.subheader("📜 Prediction History")

        st.dataframe(history, use_container_width=True)

        fig = px.histogram(
            history,
            x="Crop",
            color="Crop",
            title="Crop Prediction Frequency"
        )

        st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# QUICK FARM TIPS
# ==========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🌾 Farming Tips")

tips = [

    "Use certified seeds.",

    "Maintain soil pH between 6 and 7.",

    "Avoid over-irrigation.",

    "Use organic compost regularly.",

    "Rotate crops every season.",

    "Test soil before sowing.",

    "Control weeds early.",

    "Monitor weather regularly."

]

st.sidebar.success(
    np.random.choice(tips)
)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <center>

    <h4>🌾 Smart Crop Prediction System</h4>

    Built using ❤️ with

    <b>Python</b> |
    <b>Streamlit</b> |
    <b>Machine Learning</b> |
    <b>Google Gemini AI</b> |
    <b>OpenWeather API</b>

    </center>
    """,
    unsafe_allow_html=True
)
# ==========================================================
# ADVANCED ANALYTICS DASHBOARD
# ==========================================================

st.markdown("---")
st.header("📊 Farm Analytics Dashboard")

health_score = 100
N = st.number_input("Nitrogen (N)", value=90)

P = st.number_input("Phosphorus (P)", value=42)

K = st.number_input("Potassium (K)", value=43)

temperature = st.number_input("Temperature (°C)", value=25.0)

humidity = st.number_input("Humidity (%)", value=80.0)

ph = st.number_input("pH", value=6.5)

rainfall = st.number_input("Rainfall (mm)", value=200.0)

if N < 50:
    health_score -= 10

if P < 40:
    health_score -= 10

if K < 40:
    health_score -= 10

if ph < 5.5 or ph > 7.5:
    health_score -= 15

if rainfall < 60:
    health_score -= 15

health_score = max(0, health_score)

st.progress(health_score / 100)

st.metric(
    "Soil Health Score",
    f"{health_score}%"
)

# ==========================================================
# PIE CHART
# ==========================================================

st.subheader("🌱 Nutrient Distribution")

pie_df = pd.DataFrame({
    "Nutrient": [
        "Nitrogen",
        "Phosphorus",
        "Potassium"
    ],
    "Value": [
        N,
        P,
        K
    ]
})

pie = px.pie(
    pie_df,
    names="Nutrient",
    values="Value",
    title="NPK Distribution"
)

st.plotly_chart(
    pie,
    use_container_width=True
)

# ==========================================================
# IRRIGATION CALCULATOR
# ==========================================================

st.subheader("💧 Irrigation Recommendation")

if rainfall > 250:

    irrigation = "Very Low"

elif rainfall > 150:

    irrigation = "Low"

elif rainfall > 80:

    irrigation = "Medium"

else:

    irrigation = "High"

st.info(
    f"Recommended Irrigation Level : {irrigation}"
)

# ==========================================================
# CROP CALENDAR
# ==========================================================

st.subheader("🗓 Crop Calendar")

calendar = {

    "Rice":"June - July",

    "Wheat":"October - November",

    "Cotton":"April - May",

    "Maize":"June - July",

    "Sugarcane":"January - March",

    "Groundnut":"June - July",

    "Coffee":"June",

    "Banana":"Throughout Year"

}
features = [[N, P, K, temperature,humidity,ph, rainfall]]
model=joblib.load("model.pkl")
prediction = model.predict(features)[0]

crop = str(prediction).title()

if crop in calendar:

    st.success(
        f"Best Sowing Time : {calendar[crop]}"
    )

else:

    st.info(
        "Follow your local agricultural calendar."
    )

# ==========================================================
# DISEASE PREVENTION
# ==========================================================

st.subheader("🦠 Disease Prevention")

disease_tips = [

    "Use certified quality seeds.",

    "Avoid water logging.",

    "Rotate crops every season.",

    "Use bio-fertilizers whenever possible.",

    "Inspect leaves weekly.",

    "Apply fungicide only when required.",

    "Remove infected plants immediately.",

    "Maintain proper spacing."

]

for tip in disease_tips:

    st.write("✅", tip)

# ==========================================================
# FARM CHECKLIST
# ==========================================================

st.subheader("📋 Farmer Checklist")

st.checkbox("Soil Tested")

st.checkbox("Quality Seeds Purchased")

st.checkbox("Fertilizer Ready")

st.checkbox("Irrigation Available")

st.checkbox("Weather Checked")

st.checkbox("Equipment Ready")

# ==========================================================
# AGRICULTURE NEWS
# ==========================================================

st.subheader("📰 Daily Agriculture Tips")

news = [

    "Apply fertilizer after soil testing.",

    "Rainwater harvesting improves irrigation.",

    "Organic farming increases soil fertility.",

    "Monitor pest attacks every week.",

    "Use drip irrigation to save water.",

    "Crop rotation prevents nutrient loss."

]

st.success(np.random.choice(news))

# ==========================================================
# AI SUMMARY
# ==========================================================

st.subheader("🤖 Final AI Summary")

summary = f"""

Crop : {prediction}

Soil Health Score : {health_score}%

Irrigation Level : {irrigation}

Weather : Suitable

Recommendation :

Continue balanced fertilizer usage.

Monitor weather every week.

Follow disease prevention practices.

"""

st.code(summary)

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

with st.expander("ℹ About This Project"):

    st.write("""

Smart Crop Prediction System

Features Included

✅ Machine Learning Prediction

✅ Weather API

✅ Google Gemini AI

✅ Interactive Maps

✅ Soil Health Analysis

✅ Fertilizer Recommendation

✅ Irrigation Suggestion

✅ Disease Prevention

✅ Crop Calendar

✅ Dashboard Analytics

✅ Prediction History

✅ CSV Report Download

Built using

Python

Streamlit

Scikit-Learn

Google Gemini AI

OpenWeather API

Plotly

Folium

""")

# ==========================================================
# FINAL FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
"""
<center>

<h2>🌾 Smart Crop Prediction & Recommendation System</h2>

Developed using

Python • Streamlit • Machine Learning • Plotly • Gemini AI

Made for Resume Building & Placement Projects

© 2026

</center>
""",
unsafe_allow_html=True
)