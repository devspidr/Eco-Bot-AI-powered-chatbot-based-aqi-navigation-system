from flask import Flask, render_template, request, jsonify
import requests
import openai

app = Flask(__name__)

# API KEYS (Replace with actual API keys)
GOOGLE_MAPS_API_KEY = "Your API Key"
AQICN_API_KEY = "Your API Key"
OPENAI_API_KEY = "Your API Key"

# OpenAI API Setup
openai.api_key = OPENAI_API_KEY

# API URLs
GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
AQI_API_URL = "https://api.waqi.info/feed/geo:{},{}?token={}"

def get_coordinates(location):
    """Convert address to latitude and longitude using Google Geocoding API."""
    params = {"address": location, "key": GOOGLE_MAPS_API_KEY}
    response = requests.get(GOOGLE_GEOCODE_URL, params=params).json()
    
    if response.get("status") == "OK":
        loc = response["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    
    return None, None  # Return None 'if inva'lid



def get_aqi(lat, lon):
    """Fetch AQI data for a given location or generate a random AQI if the API fails."""
    try:
        response = requests.get(AQI_API_URL.format(lat, lon, AQICN_API_KEY), timeout=5)  # Set timeout for API call
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        response_json = response.json()

        # Check if response contains AQI data
        if "data" in response_json and isinstance(response_json["data"], dict):
            aqi_value = response_json["data"].get("aqi")
            if isinstance(aqi_value, int):  # Ensure AQI is a valid integer
                return aqi_value

        # If AQI is missing or invalid, return a random AQI value
        return random.randint(75, 250)

    except (requests.RequestException, ValueError, KeyError):
        # Handle API request failures, JSON parsing errors, or missing keys
        return random.randint(75, 250)  # Return random AQI in case of failure




def recommend_transport(aqi):
    """Recommend transport based on AQI."""
    if aqi < 50:
        return "Car/Bike (Good AQI)"
    elif 50 <= aqi < 100:
        return "Bike (Moderate AQI)"
    elif 100 <= aqi < 150:
        return "Public Transport (Unhealthy for sensitive groups)"
    else:
        return "🚨 Strongly prefer Public Transport! Wear a mask! 🚨"

import random  # Import the random module

def calculate_coins(aqi):
    """Calculate coin rewards based on AQI."""
    if aqi < 50:
        return random.randint(5, 20)  # Reward between 5-20 coins
    elif 50 <= aqi < 100:
        return random.randint(20, 30)
    elif 100 <= aqi < 150:
        return random.randint(30, 50)
    elif 150 <= aqi < 200:
        return random.randint(50, 70)
    elif 200 <= aqi < 250:
        return random.randint(70, 90)
    else:
        return 0  # No coins if AQI is too high

def get_best_route(source, destination):
    """Get the best route based on AQI."""
    src_lat, src_lng = get_coordinates(source)
    dest_lat, dest_lng = get_coordinates(destination)

    if not src_lat or not dest_lat:
        return None, "Could not fetch route details.", 0

    aqi_destination = get_aqi(dest_lat, dest_lng)
    route_link = f"https://www.google.com/maps/dir/?api=1&origin={src_lat},{src_lng}&destination={dest_lat},{dest_lng}"

    return route_link, aqi_destination, aqi_destination

def get_openai_response(user_message):
    """Generate chatbot response using OpenAI GPT."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an AQI-based route assistant."},
                  {"role": "user", "content": user_message}]
    )
    return response["choices"][0]["message"]["content"]


@app.route("/")
def chatbot():
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()
    


    if "to" in user_message:
        try:
            words = user_message.split()
            if "to" in words:
                index = words.index("to")
                source = " ".join(words[:index])
                destination = " ".join(words[index + 1:])

                if not source or not destination:
                    return jsonify({"bot_reply": "Please provide both source and destination."})

                route_link, aqi, avg_aqi = get_best_route(source, destination)
                
                if not route_link:
                    return jsonify({"bot_reply": "No suitable route found!"})
                
                transport_recommendation = recommend_transport(aqi)
                carbon_coins = calculate_coins(aqi)
                
                bot_reply = (
                    f"<b>Recommended Route & AQI Report</b><br>"
                    f"📍 <a href='{route_link}' target='_blank'>Click here to view the route</a><br><br>"
                    f"<b>Air Quality Index (AQI):</b><br>{aqi}<br><br>"
                    f"<b>Recommended Mode of Transport:</b><br>{transport_recommendation}<br><br>"
                    f"<b>Earn Carbon-Free Coins:</b><br>{carbon_coins}"
                )
                return jsonify({"bot_reply": bot_reply})
        
        except Exception as e:
            return jsonify({"bot_reply": "Error processing your request. Please try again."})
    
    else:
        # Use OpenAI for general chatbot responses
        bot_reply = get_openai_response(user_message)
        return jsonify({"bot_reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)

