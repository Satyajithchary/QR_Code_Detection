pip install streamlit opencv-python-headless pyzbar numpy pillow
import streamlit as st
import os
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

# Function to decode QR codes
def decode_qr(image):
    qr_info = decode(image)
    decoded_data = []
    for qr in qr_info:
        data = qr.data.decode('utf-8')
        rect = qr.rect
        polygon = qr.polygon
        decoded_data.append((data, rect, polygon))
        # Draw rectangle and polygon on the image
        image = cv2.rectangle(image, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
                              (0, 255, 0), 2)
        image = cv2.polylines(image, [np.array(polygon)], True, (255, 0, 0), 2)
    return image, decoded_data

# Streamlit app
st.title("QR Code Decoder")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Decode QR code
    decoded_img, decoded_data = decode_qr(img)

    st.image(img_rgb, caption='Uploaded Image', use_column_width=True)
    st.image(decoded_img, caption='Decoded Image with Annotations', use_column_width=True)

    st.subheader("Decoded Data")
    if decoded_data:
        for data, rect, polygon in decoded_data:
            st.text(f"Data: {data}")
            st.text(f"Rectangle: {rect}")
            st.text(f"Polygon: {polygon}")
    else:
        st.text("No QR code found in the image.")

