import streamlit as st
import requests
import base64
import time
import os
from dotenv import load_dotenv
load_dotenv()

# Constants (read from environment variables)
IMAGEKIT_UPLOAD_URL = os.environ.get("IMAGEKIT_UPLOAD_URL")
IMAGEKIT_PUBLIC_KEY = os.environ.get("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_PRIVATE_KEY = os.environ.get("IMAGEKIT_PRIVATE_KEY")
FASHN_API_RUN_URL = os.environ.get("FASHN_API_RUN_URL")
FASHN_API_STATUS_URL = os.environ.get("FASHN_API_STATUS_URL")
FASHN_API_KEY = os.environ.get("FASHN_API_KEY")

# Upload images to ImageKit
def upload_to_imagekit(file):
    """Uploads an image to ImageKit.io and returns the direct URL."""
    encoded_auth = base64.b64encode(f"{IMAGEKIT_PRIVATE_KEY}:".encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_auth}"
    }
    response = requests.post(
        IMAGEKIT_UPLOAD_URL,
        files={"file": file},
        data={"fileName": file.name},
        headers=headers
    )
    if response.status_code == 200:
        return response.json()["url"]
    else:
        st.error(f"ImageKit upload failed: {response.json()}")
        return None

# Submit virtual try-on request
def post_virtual_try_on(model_image_url, garment_image_url, category):
    """Posts a request to Fashn.ai for virtual try-on."""
    payload = {
        "model_image": model_image_url,
        "garment_image": garment_image_url,
        "category": category
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FASHN_API_KEY}"
    }
    response = requests.post(FASHN_API_RUN_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        st.error(f"POST request failed: {response.json()}")
        return None

# Get virtual try-on result
def get_prediction_status(prediction_id):
    """Polls the status endpoint to retrieve the result."""
    headers = {"Authorization": f"Bearer {FASHN_API_KEY}"}
    url = f"{FASHN_API_STATUS_URL}/{prediction_id}"
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            status = data["status"]
            if status == "completed":
                return data["output"]
            elif status == "failed":
                st.error(f"Prediction failed: {data['error']}")
                return None
            else:
                st.info(f"Processing: {status}")
                time.sleep(5)
        else:
            st.error(f"Failed to retrieve result: {response.json()}")
            return None

# Streamlit App
def main():
    # Page settings
    st.set_page_config(page_title="House of Mahalasa - Virtual Try-On", layout="wide")

    # Branding
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Roboto:wght@400;500&display=swap" rel="stylesheet">
        <style>
        body {
            background: linear-gradient(135deg, #f8fafc 0%, #e0c3fc 100%);
            font-family: 'Roboto', Arial, sans-serif;
        }
        .header {
            background: linear-gradient(90deg, #8e2de2 0%, #4a00e0 100%);
            padding: 32px 0 18px 0;
            text-align: center;
            font-size: 44px;
            font-weight: bold;
            font-family: 'Montserrat', Arial, sans-serif;
            color: #fff;
            border-radius: 0 0 32px 32px;
            box-shadow: 0 6px 24px rgba(76,0,255,0.10);
            letter-spacing: 2px;
        }
        .subheader {
            text-align: center;
            font-size: 22px;
            color: #4a00e0;
            margin-top: 0;
            margin-bottom: 32px;
            font-family: 'Roboto', Arial, sans-serif;
            font-weight: 500;
        }
        .upload-box {
            background: #fff;
            padding: 32px 24px 24px 24px;
            border-radius: 18px;
            box-shadow: 0 8px 32px rgba(76,0,255,0.10), 0 1.5px 6px rgba(0,0,0,0.04);
            max-width: 520px;
            margin: 0 auto 32px auto;
            border: 1.5px solid #e0c3fc;
        }
        .stButton>button {
            background: linear-gradient(90deg, #8e2de2 0%, #4a00e0 100%);
            color: #fff;
            font-size: 20px;
            font-family: 'Montserrat', Arial, sans-serif;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 12px 32px;
            margin-top: 12px;
            box-shadow: 0 2px 8px rgba(76,0,255,0.10);
            transition: background 0.3s, transform 0.2s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #4a00e0 0%, #8e2de2 100%);
            transform: translateY(-2px) scale(1.03);
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 14px;
            color: #8e2de2;
            font-family: 'Roboto', Arial, sans-serif;
            letter-spacing: 1px;
        }
        .result-card {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 8px 32px rgba(76,0,255,0.10), 0 1.5px 6px rgba(0,0,0,0.04);
            padding: 24px;
            margin: 24px auto;
            max-width: 600px;
            text-align: center;
        }
        .result-card img {
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(76,0,255,0.08);
            margin-bottom: 12px;
        }
        .upload-label {
            font-size: 18px;
            color: #4a00e0;
            font-family: 'Montserrat', Arial, sans-serif;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .stFileUploader {
            margin-bottom: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Logo/branding (optional, placeholder for now)
    st.markdown(
        '<div style="text-align:center;margin-bottom:12px;">'
        '<img src="https://i.imgur.com/8Km9tLL.png" alt="Logo" width="90" style="border-radius:18px;box-shadow:0 2px 8px rgba(76,0,255,0.10);margin-bottom:0;">'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="header">House of Mahalasa</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Experience the future of fashion with our Virtual Try-On application.</div>', unsafe_allow_html=True)

    # Upload section
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    st.markdown('<div class="upload-label">Upload Model Image (JPG/PNG)</div>', unsafe_allow_html=True)
    model_image = st.file_uploader("", type=["jpg", "jpeg", "png"], key="model")
    st.markdown('<div class="upload-label">Upload Garment Image (JPG/PNG)</div>', unsafe_allow_html=True)
    garment_image = st.file_uploader("", type=["jpg", "jpeg", "png"], key="garment")
    st.markdown('</div>', unsafe_allow_html=True)

    # Preview uploaded images
    if model_image is not None or garment_image is not None:
        st.markdown(
            """
            <div style="display: flex; flex-direction: row; justify-content: center; align-items: flex-start; gap: 48px; margin-bottom: 24px; flex-wrap: wrap;">
                <div style="text-align:center; min-width: 220px; max-width: 260px;">
                    <span style="font-size:16px;color:#4a00e0;font-family:Montserrat;font-weight:600;">Model Image Preview</span><br>
                    """ + (f'<img src="data:image/png;base64,{base64.b64encode(model_image.read()).decode()}" width="220" style="border-radius:12px;box-shadow:0 2px 8px rgba(76,0,255,0.10);margin-top:8px;">' if model_image is not None else '') + """
                </div>
                <div style="text-align:center; min-width: 220px; max-width: 260px;">
                    <span style="font-size:16px;color:#4a00e0;font-family:Montserrat;font-weight:600;">Garment Image Preview</span><br>
                    """ + (f'<img src="data:image/png;base64,{base64.b64encode(garment_image.read()).decode()}" width="220" style="border-radius:12px;box-shadow:0 2px 8px rgba(76,0,255,0.10);margin-top:8px;">' if garment_image is not None else '') + """
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Reset file pointer for Streamlit to re-read the files later
        if model_image is not None:
            model_image.seek(0)
        if garment_image is not None:
            garment_image.seek(0)

    # Garment category selection
    category_display = {
        "Tops": "tops",
        "Bottoms": "bottoms",
        "Dresses / One-Pieces": "one-pieces",
        "Auto": "auto"
    }
    category_choice = st.radio(
        "Select Garment Category",
        options=list(category_display.keys()),
        index=0,
        horizontal=True,
        help="Choose the type of garment for virtual try-on.",
    )
    category = category_display[category_choice]

    # Action button
    if st.button("Generate Virtual Try-On"):
        if model_image and garment_image:
            st.info("Uploading images to ImageKit.io...")
            model_image_url = upload_to_imagekit(model_image)
            garment_image_url = upload_to_imagekit(garment_image)

            if model_image_url and garment_image_url:
                st.success("Images uploaded successfully!")
                st.info("Processing virtual try-on request...")
                prediction_id = post_virtual_try_on(model_image_url, garment_image_url, category)

                if prediction_id:
                    st.success("Request submitted successfully!")
                    st.info("Fetching results...")
                    result = get_prediction_status(prediction_id)

                    if result:
                        st.success("Virtual Try-On Completed!")
                        for url in result:
                            st.markdown('<div class="result-card">', unsafe_allow_html=True)
                            st.image(url, caption="Try-On Result", use_column_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("Failed to retrieve try-on result.")
            else:
                st.error("Image upload failed. Please try again.")
        else:
            st.warning("Please upload both model and garment images.")

    # Footer
    st.markdown('<div class="footer">Powered by House of Mahalasa</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
