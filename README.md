# EcoBot 🌱

Welcome to the **EcoBot** project! This is an **AI-powered chatbot-based navigation system** designed to promote eco-friendly travel by providing users with the best routes based on air quality index (AQI) and recommending sustainable transportation options. Whether you're a developer, environmental enthusiast, or just curious, we're excited to have you here!
 
 
## 📌 Project Overview

EcoBot is a **smart navigation assistant** that helps users find the best travel routes while considering environmental factors like air quality. It integrates **Google Maps API** for route planning, **AQI data** for air quality analysis, and **OpenAI GPT** for intelligent chatbot interactions. The goal is to encourage users to adopt eco-friendly travel habits and reduce their carbon footprint.

## ✨ Features

- 🌬️ **AQI-Based Route Recommendations**: Get the best travel routes based on real-time air quality data.
- 🚴 **Transportation Recommendations**: EcoBot suggests the most eco-friendly mode of transport (e.g., public transport, biking) based on AQI levels.
- 💚 **Carbon-Free Coins**: Earn rewards for choosing eco-friendly routes and transportation options.
- 💬 **Interactive Chatbot**: A user-friendly chatbot interface powered by OpenAI GPT for seamless interaction.
- 📡 **Real-Time AQI Data**: Fetch and display the Air Quality Index (AQI) for any destination.
- 🗺️ **Google Maps Integration**: View recommended routes directly on Google Maps.

## ⚙️ Installation

To set up **EcoBot** locally, follow these steps:

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/EcoBot.git
cd EcoBot
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables
Create a .env file in the root directory and add the following keys:
```bash
GOOGLE_MAPS_API_KEY="AIzaSyATWInFL0lPFJcCUE5DSZmtFG5SpANaCrA"
AQICN_API_KEY="f99b778a6ca3623d12fcab9584a90095131c920d"
OPENAI_API_KEY="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"
```

### 4️⃣ Run the application
```bash
python app.py
```

### 5️⃣ Access the application
```bash
http://127.0.0.1:5000
```
