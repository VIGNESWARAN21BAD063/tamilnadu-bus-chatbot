import streamlit as st
from deep_translator import GoogleTranslator

# Bus data
bus_data = {
    ("chennai", "madurai"): {"timing": "6:00 AM, 12:00 PM, 6:00 PM", "fare": "₹350"},
    ("chennai", "coimbatore"): {"timing": "5:30 AM, 1:00 PM, 9:00 PM", "fare": "₹400"},
    ("chennai", "dharmapuri"): {"timing": "6:45 AM, 2:15 PM, 10:30 PM", "fare": "₹320"},
    ("madurai", "trichy"): {"timing": "7:00 AM, 1:30 PM, 7:00 PM", "fare": "₹220"},
    ("trichy", "coimbatore"): {"timing": "6:15 AM, 2:00 PM, 8:30 PM", "fare": "₹280"},
}

# Extract place names
places = list({p for route in bus_data for p in route})

# Extract source and destination from user query
def extract_places(text):
    found = [p for p in places if p in text]
    if len(found) >= 2:
        return found[0], found[1]
    elif len(found) == 1:
        return found[0], None
    else:
        return None, None

# Chatbot response logic
def chatbot_reply(query):
    query = query.lower()
    from_place, to_place = extract_places(query)

    if not from_place or not to_place:
        return "❗ Please mention both **source** and **destination** (e.g., 'Chennai to Madurai')."

    route = (from_place, to_place)
    if route in bus_data:
        info = bus_data[route]
    elif (to_place, from_place) in bus_data:
        info = bus_data[(to_place, from_place)]
    else:
        return f"🚫 Sorry, we don't have data for **{from_place.title()} to {to_place.title()}**."

    return f"🚌 **Bus Timing:** {info['timing']}\n💸 **Ticket Fare:** {info['fare']}"


# Streamlit UI
st.title("🚌 Tamil Nadu Public Transport Chatbot")

user_input = st.text_input("Ask your transport question in any language:")

if user_input:
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(user_input)
        response = chatbot_reply(translated)
        st.success(response)
    except Exception as e:
        st.error(f"⚠️ Error: {e}")



