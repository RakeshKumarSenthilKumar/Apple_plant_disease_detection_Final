import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import tempfile

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyBLGohpipKfhQ17IsILLOGNT3m7l9jeoOs"
genai.configure(api_key=GEMINI_API_KEY)

PLANT_KEYWORDS = [
    # Basic Plant Anatomy
    "plant", "plants", "tree", "trees", "flower", "flowers", "leaf", "leaves",
    "stem", "stems", "root", "roots", "fruit", "fruits", "seed", "seeds", "bud", "buds",
    "branch", "trunk", "shoot", "sprout", "bark", "blossom", "petal", "pollen", "pollinator",
    "germination", "photosynthesis", "chlorophyll", "vascular tissue", "xylem", "phloem",

    # Diseases & Pests
    "plant disease", "fungal infection", "bacterial infection", "viral disease", "leaf spot",
    "powdery mildew", "downy mildew", "blight", "wilt", "canker", "scab", "rot", "root rot",
    "stem rot", "black rot", "rust", "mosaic virus", "chlorosis", "necrosis", "yellowing",
    "curling leaves", "wilting", "aphids", "mites", "thrips", "caterpillars", "nematodes",
    "fungus gnats", "whiteflies", "mealybugs", "scale insects", "snails", "slugs",

    # Gardening & Plant Care
    "gardening", "horticulture", "botany", "plant care", "watering", "fertilizing", "pruning",
    "deadheading", "mulching", "repotting", "planting", "sowing", "weeding", "thinning",
    "staking", "grafting", "cuttings", "division", "transplanting", "soil testing",
    "compost", "organic compost", "vermicompost", "potting mix", "peat moss", "cocopeat",
    "perlite", "hydroponics", "aeroponics", "grow lights", "indoor plants", "houseplants",
    "greenhouse", "nursery", "terrarium", "bonsai", "planter", "shade-loving", "sun-loving",

    # Plant Types
    "herb", "shrubs", "shrub", "tree", "vine", "climber", "creeper", "grass", "succulent", 
    "cactus", "aquatic plant", "flowering plant", "non-flowering plant", "annual", "biennial", 
    "perennial", "deciduous", "evergreen", "orchid", "fern", "palm", "bulb", "tuber", "rhizome",

    # Fruits, Vegetables & Crops
    "apple", "banana", "mango", "grape", "papaya", "pear", "plum", "orange", "guava", "melon",
    "watermelon", "lemon", "lime", "pineapple", "tomato", "potato", "onion", "carrot",
    "spinach", "cabbage", "cauliflower", "chili", "pepper", "peas", "beans", "okra", "radish",
    "turnip", "pumpkin", "zucchini", "brinjal", "eggplant", "beetroot", "lettuce", "garlic",
    "ginger", "turmeric", "coriander", "curry leaf", "basil", "mint", "thyme", "rosemary",

    # Soil & Environment
    "soil", "clay soil", "sandy soil", "loamy soil", "fertile soil", "soil pH", "moisture",
    "humidity", "drainage", "sunlight", "shade", "temperature", "climate", "frost", "drought",
    "monsoon", "rainfall", "seasons", "growing season", "microclimate",

    # Sustainable & Organic Farming
    "organic", "organic farming", "pesticide", "herbicide", "fungicide", "biodegradable",
    "natural remedy", "pest control", "eco-friendly", "biological control", "sustainability",
    "companion planting", "crop rotation", "green manure", "mulch", "cover crop", "agroforestry",

    # Tools & Accessories
    "watering can", "sprayer", "shovel", "spade", "hoe", "trowel", "gloves", "fertilizer",
    "planter box", "hanging pot", "drip irrigation", "garden hose", "seed tray", "grow bag",
    "propagation tray", "humidity dome", "grow tent", "UV light", "garden scissors",

    # Botanical Processes
    "transpiration", "plant hormones", "auxins", "cytokinins", "gibberellins", "abscisic acid",
    "ethylene", "photoperiodism", "tropism", "gravitropism", "phototropism", "plant physiology",

    # Misc
    "crop", "harvest", "yield", "plant propagation", "landscape", "agronomy", "vegetation",
    "ecosystem", "reforestation", "pollution impact", "plant biodiversity", "weeds", "allelopathy"
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
