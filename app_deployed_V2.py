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

filenames = os.listdir("./img_p8")

imgs = [filename for filename in filenames if filename.endswith('leftImg8bit.png')]
masks = [filename for filename in filenames if filename.endswith('gtFine_labelIds.png')]

indexes = list(range(len(imgs)))
index = st.selectbox('Selectionnez une image:', indexes)

st.write("Image :", imgs[index])
st.write("Masque : ", masks[index])

img_pil = Image.open("./img_p8/" + imgs[index])
mask_pil = Image.open("./img_p8/" + masks[index])
img_pil_bytes = open("./img_p8/" + imgs[index], 'rb')

# url = 'https://image-segmentation-test.azurewebsites.net/predict_mask'
url = 'https://image-segmentation-test.azurewebsites.net/predict_mask/'
# url = "http://127.0.0.1:8000/"

predict_btn = st.button('Predict')
if predict_btn:
        files = {'file': img_pil_bytes}
        response = requests.post(url, files=files)
        st.write(response)

        # Get images to JSON format
        result = response.json()

        # Get mask predicted
        predicted_mask = result["prediction"]

        # Decode mask on base64 and open it
        decoded_mask = base64.b64decode(predicted_mask)
        mask_image = Image.open(BytesIO(decoded_mask))


        st.image([img_pil, mask_pil, mask_image], caption=["Image original", "Masque réel", "Masque prédit"], width=225)

# --------------------------------------------------------------------------