from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini multimodal model
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/analyze")
async def analyze_image(
    image: UploadFile,
    question: str = Form(...),
):
    try:
        # Read image content
        image_content = await image.read()

        # Load and validate the image
        img = Image.open(io.BytesIO(image_content))
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Prompt (text comes after the image)
        prompt = f"Please answer this question about the image: {question}"

        # Generate multimodal response
        response = model.generate_content(
            contents=[
                {"mime_type": "image/jpeg", "data": image_content},
                prompt
            ],
            stream=False
        )

        return JSONResponse({
            "answer": response.text,
            "success": True
        })

    except Exception as e:
        print(f"Image analysis error: {e}")
        return JSONResponse({
            "answer": f"Image analysis failed: {str(e)}",
            "success": False
        })

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
