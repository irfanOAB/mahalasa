# House of Mahalasa - Virtual Try-On

This is a Streamlit app for virtual fashion try-on, powered by House of Mahalasa. Users can upload a model image and a garment image, select the garment category, and generate a virtual try-on result using the Fashn.ai API.

## Features

- Upload model and garment images (JPG/PNG)
- Select garment category (Tops, Bottoms, Dresses/One-Pieces, Auto)
- Images are uploaded to ImageKit.io
- Virtual try-on is performed via the Fashn.ai API
- Results are displayed directly in the app

## Running on Hugging Face Spaces

This Space uses a custom `Dockerfile` and the Streamlit SDK. Hugging Face will automatically build the Docker image and run the app using the configuration in `Dockerfile`.

1. **Clone or upload this repository to your Hugging Face Space.**
2. The following files are required:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `Dockerfile`
3. Hugging Face will automatically build the Docker image, install dependencies, and launch the app on port 7860.
4. **Set the following secrets in your Hugging Face Space:**
   - Go to your Space's "Settings" > "Secrets" tab.
   - Add the following environment variables with your own values:
     - `IMAGEKIT_UPLOAD_URL`
     - `IMAGEKIT_PUBLIC_KEY`
     - `IMAGEKIT_PRIVATE_KEY`
     - `FASHN_API_RUN_URL`
     - `FASHN_API_STATUS_URL`
     - `FASHN_API_KEY`
   - These values are required for the app to function.

## Local Development

To run locally, set the above environment variables in your shell or with a `.env` file (using a tool like `python-dotenv`):

```bash
pip install -r requirements.txt
export IMAGEKIT_UPLOAD_URL=...
export IMAGEKIT_PUBLIC_KEY=...
export IMAGEKIT_PRIVATE_KEY=...
export FASHN_API_RUN_URL=...
export FASHN_API_STATUS_URL=...
export FASHN_API_KEY=...
streamlit run app.py
```

## Notes

- All API keys and secrets are now loaded from environment variables for security. Do not hardcode secrets in the code or repository.
- This app is intended for demonstration and prototyping.