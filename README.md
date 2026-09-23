# 🌾 Smart Crop Prediction & Recommendation System

An AI-powered Crop Prediction System built with **Python**, **Streamlit**, **Machine Learning**, **Google Gemini AI**, **OpenWeather API**, **Plotly**, and **Folium**.

The application predicts the best crop based on soil parameters, weather conditions, and provides AI-powered farming recommendations.

---

# 🚀 Features

- 🌾 Crop Prediction using Machine Learning
- 🤖 Google Gemini AI Farming Assistant
- 🌦 Real-Time Weather Information
- 🗺 Interactive Farm Location Map
- 📊 Soil Nutrient Analysis
- 🌱 Soil Health Detection
- 🧪 Fertilizer Recommendation
- 💧 Irrigation Suggestion
- 🦠 Disease Prevention Tips
- 📅 Crop Calendar
- 📈 Analytics Dashboard
- 📁 Prediction History
- 📥 CSV Report Download
- 🎨 Professional Streamlit UI

---

# 🛠 Technologies Used

- Python
- Streamlit
- Scikit-Learn
- Pandas
- NumPy
- Plotly
- Folium
- Geopy
- Google Gemini API
- OpenWeather API
- Joblib
- Python Dotenv

---

# 📂 Project Structure

```
Crop_Prediction_System/
│
├── app.py
├── train_model.py
├── Crop_recommendation.csv
├── model.pkl
├── requirements.txt
├── .env
├── prediction_history.csv
└── README.md
```

---

# 📥 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Crop-Prediction-System.git
```

Go to the project folder

```bash
cd Crop-Prediction-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure API Keys

Create a `.env` file.

```env
OPENWEATHER_API_KEY=your_openweather_api_key
GEMINI_API_KEY=your_google_gemini_api_key
```

---

# 📊 Train the Model

Place the dataset

```
Crop_recommendation.csv
```

inside the project folder.

Run

```bash
python train_model.py
```

This creates

```
model.pkl
```

---

# ▶ Run the Application

```bash
streamlit run app.py
```

Open

```
http://localhost:8501
```

---

# 📊 Dataset Features

The ML model uses:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

Target:

- Crop Label

---

# 🌾 Supported Crops

- Rice
- Wheat
- Maize
- Cotton
- Jute
- Coffee
- Banana
- Mango
- Chickpea
- Kidney Beans
- Lentil
- Blackgram
- Mung Bean
- Pigeon Peas
- Coconut
- Papaya
- Orange
- Apple
- Muskmelon
- Watermelon
- Grapes
- Pomegranate

---

# 📈 Workflow

1. User enters soil values.
2. Weather is fetched from OpenWeather.
3. ML model predicts the best crop.
4. Soil health is analyzed.
5. Fertilizer recommendations are generated.
6. AI farming advice is generated using Gemini.
7. Prediction is saved.
8. User can download the report.

---

# 📷 Screens

- Dashboard
- Prediction Page
- Weather Page
- Interactive Map
- AI Assistant
- Analytics Dashboard

---

# 📦 Requirements

```
streamlit
pandas
numpy
scikit-learn
joblib
requests
plotly
folium
streamlit-folium
geopy
python-dotenv
google-generativeai
```

Install

```bash
pip install -r requirements.txt
```

---

# 👩‍💻 Developer

**Vaishnavi Santosh Kulkarni**

B.E. Artificial Intelligence & Data Science

JSPM's Jayawantrao Sawant College of Engineering, Pune

---

# 📄 License

This project is developed for educational purposes and resume building.

Feel free to modify and improve it.

---

# ⭐ Future Improvements

- Deep Learning Prediction
- Satellite Image Analysis
- Leaf Disease Detection
- Voice Assistant
- Farmer Login System
- Cloud Deployment
- Mobile Application
- Multi-language Support
- SMS Alerts
- IoT Sensor Integration

---

# ❤️ Thank You

If you like this project, don't forget to ⭐ the repository.