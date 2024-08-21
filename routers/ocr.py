from PIL import Image
from urllib import request
from fastapi import APIRouter
import pytesseract


router = APIRouter(
    prefix="/ocr",
    tags=["ocr"]
)

@router.post("/")
async def ocr_process():
    if request.method == 'POST':
        image_file = request.files['image']
        image_data = Image.open(image_file)

        # Perform OCR using PyTesseract
        text = pytesseract.image_to_string(image_data)

        response = {
            'status': 'success',
            'text': text
        }
        return response
        