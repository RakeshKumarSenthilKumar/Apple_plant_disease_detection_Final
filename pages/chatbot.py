import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import tempfile

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyBLGohpipKfhQ17IsILLOGNT3m7l9jeoOs"
genai.configure(api_key=GEMINI_API_KEY)

# Define plant-related keywords
PLANT_KEYWORDS = [
    # Basic plant parts and functions
    "plant", "tree", "flower", "leaves", "leaf", "stem", "root", "roots",
    "seed", "seeds", "bud", "bloom", "branch", "trunk", "fruit", "fruits",
    "photosynthesis", "chlorophyll", "pollination", "germination", "flowering",

    # Plant diseases and issues
    "plant disease", "fungal infection", "bacterial infection", "viral disease",
    "blight", "rot", "mildew", "rust", "canker", "wilt", "mosaic virus", 
    "leaf spot", "scab", "yellowing leaves", "plant pest", "pests", "aphids",
    "mites", "caterpillars", "insects", "infestation", "fungus gnats", "nematodes",

    # Gardening and care
    "gardening", "farming", "agriculture", "horticulture", "watering", 
    "fertilizing", "fertilization", "compost", "mulch", "soil", "soil pH",
    "drainage", "sunlight", "shade", "plant nutrients", "plant food", 
    "plant care", "repotting", "pruning", "deadheading", "planting", 
    "transplanting", "weeding", "crop rotation", "organic farming",

    # Plant growth and development
    "plant growth", "growth stages", "vegetative stage", "flowering stage", 
    "yield", "germination rate", "root development", "shoot", "sprout", "propagation",

    # Types of plants and environments
    "indoor plant", "outdoor plant", "succulent", "cactus", "orchid", 
    "fern", "herb", "shrub", "vine", "grass", "crop", "vegetable", "fruit tree",
    "houseplant", "bonsai", "terrarium", "greenhouse", "nursery", "climber",

    # Common plant names (add more as needed)
    "rose", "tomato", "potato", "mango", "banana", "apple", "spinach", "carrot",
    "marigold", "tulip", "sunflower", "basil", "mint", "chili", "onion", "cabbage",

    # Soil and climate
    "soil health", "loamy soil", "clay soil", "sandy soil", "moisture", 
    "humidity", "drought", "frost", "seasonal plants", "climate", "temperature",

    # Sustainability
    "organic", "pesticide", "herbicide", "biodegradable", "natural remedy",
    "crop protection", "eco-friendly", "permaculture"
]


def is_plant_related(prompt):
    """Check if the input text is related to plants and plant diseases."""
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in PLANT_KEYWORDS)

def get_plant_response(prompt):
    """Get response from Gemini API if the prompt is related to plants."""
    if is_plant_related(prompt):
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    else:
        return "I only respond to plant-related queries. Please ask something about plants or plant diseases."

def generate_speech(text):
    """Convert the given text to speech and return the audio content as a byte object."""
    tts = gTTS(text=text, lang='en')
    
    # Save to temp file first to ensure proper format
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_file:
        tts.save(temp_file.name)
        temp_file.seek(0)
        audio_data = temp_file.read()

    audio_fp = BytesIO(audio_data)
    return audio_fp

# Streamlit UI
st.title("🌱 Plant Chatbot")
st.write("Ask me anything about plants, plant diseases, and plant care!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(f"**You:** {msg['text']}")
    else:
        st.chat_message("bot").markdown(f"**Bot:** {msg['text']}")

        # Button to play bot response as audio
        if st.button("🔊 Listen", key=msg["text"]):
            audio_file = generate_speech(msg["text"])
            st.audio(audio_file, format="audio/mp3")

# Input area
user_input = st.text_area("Enter your question:")

if st.button("Ask"):
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "text": user_input})

        response = get_plant_response(user_input)

        st.session_state.messages.append({"role": "bot", "text": response})

        st.rerun()
    else:
        st.warning("Please enter a question.")

# Footer
st.markdown("---")
st.markdown("🌿 *Powered by Gemini AI & Streamlit*")
