
import streamlit as st
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import google.generativeai as genai


# Setup Gemini API
GEMINI_API_KEY = "AIzaSyBLGohpipKfhQ17IsILLOGNT3m7l9jeoOs"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# Define your model
class PlantDiseaseCNN(nn.Module):
    def __init__(self, num_classes):
        super(PlantDiseaseCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * 56 * 56, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 32 * 56 * 56)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Load your trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# num_classes = 4  # Update based on your training
num_classes = 5  # Previously 4, now 5 including "Unknown"

model = PlantDiseaseCNN(num_classes)
model.load_state_dict(torch.load("pages/Plant_disease_model_with_five_class.pth", map_location=device))
model.to(device)
model.eval()


idx_to_class = {
    
    0: "Apple___Apple_scab",
    1: "Apple___Black_rot",
    2: "Apple___Cedar_apple_rust",
    3: "Apple___healthy",
    4: "Unknown"
}

# Define transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Streamlit UI
st.title("🍎 Apple Leaf Disease Detector")
st.write("Upload an image of an apple leaf to detect disease and get solutions.")
col1, col2 = st.columns([1, 10])

# import os

# col1, col2 = st.columns([1, 10])

# with col1:
#     if st.button("🎙️ Open Voice Chat"):
#         os.system('start cmd /k "streamlit run Voice-app.py"')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Leaf Image", use_column_width=True)

    if st.button("🔍 Analyze"):
        input_img = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(input_img)
            # _, predicted = torch.max(output, 1)
            probabilities = F.softmax(output, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        print("/\/\/\/\/\.")
        print(confidence.item())
        predictedthreshold =confidence.item()
        # predicted_class = idx_to_class[predicted.item()]
        # threshold = 0.6  # You can adjust this value
        # if confidence.item() < threshold:
        #     predicted_class = "Unknown"
        # else:
        #     predicted_class = idx_to_class[predicted.item()]
        # print("--------------------------")
        # print(predicted_class)
        predicted_class = idx_to_class[predicted.item()]

        #result = "scab" if predicted_class == "Apple___Apple_scab" else "Black rot" if predicted_class == "Apple___Black_rot" else  "Cedar apple rust" if predicted_class == "Apple___Cedar_apple_rust" else  "Healthy" if predicted_class == "Apple___healthy" else "Others..."
        result = (
            "scab" if predicted_class == "Apple___Apple_scab" else
            "Black rot" if predicted_class == "Apple___Black_rot" else
            "Cedar apple rust" if predicted_class == "Apple___Cedar_apple_rust" else
            "Healthy" if predicted_class == "Apple___healthy" else
            "Unknown"
        )

        st.success(f"threshold:{predictedthreshold}")
        st.success(f"✅ Predicted class: {predicted_class}")
        st.info(f"🧠 Disease detected: **{result}**")


        # Condition_prompt = f"""Analyse the given image and give me the result is "Yes" if the image is an apple leaf.Else print "No".
        #                     Note:The answer must Yes or No """
        # Condition_response = gemini_model.generate_content([Condition_prompt, image])

        # st.subheader("🌱 AI Suggestion:")
        # st.write(Condition_response.text)
        # if Condition_response.text=="No":
        #     st.warning(f"The image is Not an Apple leaf")
        # else:
        #     st.success(f"✅ Predicted class: {predicted_class}")
        #     st.info(f"🧠 Disease detected: **{result}**")
        #     if result == "Healthy":
        #         prompt = "I find my apple tree is healthy by the leaf of the apple plant. Give some suggestion to improve the health of my apple plant."
        #     else:
        #         prompt = f"""
        #         My apple tree is affected by {result}. I find it by the leaf of the apple plant.Also take the below image and find the level of disease in that leaf. Analyse that problem and give solution for that problem. Give the output like below format:

        #         Problem: "The problem of apple tree"
             
        #         Rate:level of disease in that leaf out of 100%
                
        #         Reason: "Reason for that problem of apple tree"
                
        #         Solution: "How to solve that problem"

        #         I need the output as a normal text and stricktly fallow the above formate.
        #         Make sure each label (Problem, Rate, Reason, Solution) is on its own line . The output should be plain text, not in a single paragraph, and strictly follow the format above.
        #         """

        #     # Get response from Gemini
        #     #response = gemini_model.generate_content(prompt)
        #     response = gemini_model.generate_content([prompt, image])

        #     st.subheader("🌱 AI Suggestion:")
        #     st.write(response.text)

        ###


        # st.subheader("🌱 AI Suggestion:")

        if result=="Unknown":
            st.warning(f"The image is Not an Apple leaf")
        else:
            #st.info(f"🧠 Disease detected: **{result}**")
            if result == "Healthy":
                prompt = "I find my apple tree is healthy by the leaf of the apple plant. Give some suggestion to improve the health of my apple plant."
            else:
                prompt = f"""
                My apple tree is affected by {result}. I find it by the leaf of the apple plant.Also take the below image and find the level of disease in that leaf. Analyse that problem and give solution for that problem. Give the output like below format:

                Problem: "The problem of apple tree"
             
                Rate:level of disease in that leaf out of 100%
                
                Reason: "Reason for that problem of apple tree"
                
                Solution: "How to solve that problem"

                I need the output as a normal text and stricktly fallow the above formate.
                Make sure each label (Problem, Rate, Reason, Solution) is on its own line . The output should be plain text, not in a single paragraph, and strictly follow the format above.
                """

            # Get response from Gemini
            #response = gemini_model.generate_content(prompt)
            response = gemini_model.generate_content([prompt, image])

            st.subheader("🌱 AI Suggestion:")
            st.write(response.text)
        ###
###################################
# Back to Home button
# st.markdown("---")
# if st.button("🔙 Back to Home", use_container_width=True):
#     st.switch_page("main")  # or "../Home.py" depending on structure
