# ------------------------- Imports Libraries ------------------------------

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64 
import os

# --------------------------------------------------------------------------




# ---------------------- Streamlit's application ---------------------------

st.title("Application de segmentation d'image")

#  Access the file in which the original images and original masks are located
filenames = os.listdir("./img_p8")

# Original images and original masks list sorted
images = sorted([filename for filename in filenames if filename.endswith('leftImg8bit.png')])
masks = sorted([filename for filename in filenames if filename.endswith('gtFine_labelIds.png')])

# Selection of index in list of original images and original masks
indexes = list(range(len(images)))
index = st.selectbox('Selectionnez une image:', indexes)

# Name of current original image and original mask
st.write("Image :", images[index])
st.write("Masque : ", masks[index])

# Get selected original image, original mask and predicted mask
original_image = Image.open("./img_p8/" + images[index])
original_mask = Image.open("./img_p8/" + masks[index])
mask_prediction = open("./img_p8/" + images[index], 'rb')

# URL of API
url = 'https://image-segmentation-test.azurewebsites.net/predict_mask/'

# Button for prediction
bouton_predict = st.button('Prediction')

if bouton_predict:

        # API response to get the predicted mask
        files = {'file': mask_prediction}
        response = requests.post(url, files=files)
        st.write(response)

        # Get mask predicted to JSON format
        result = response.json()

        # Get mask predicted
        predicted_mask = result["prediction"]

        # Decode mask on base64 and open it
        decoded_mask = base64.b64decode(predicted_mask)
        mask_predicted = Image.open(BytesIO(decoded_mask))

        # Display original image, original mask and predicted mask
        st.image([original_image, original_mask, mask_predicted], caption=["Image original", "Masque original", "Masque prédit"], width=225)

# --------------------------------------------------------------------------