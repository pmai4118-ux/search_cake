# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import PIL.Image
import io
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lấy key từ biến môi trường của Server
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 
if not GOOGLE_API_KEY:
    raise ValueError("Chưa cấu hình GOOGLE_API_KEY trên server!")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.get("/") # Hàm này để giảng viên bấm vào link check xem server sống hay chết
def home():
    return {"status": "Server đang chạy ngon lành!"}

@app.post("/scan-image")
async def scan_image(file: UploadFile = File(...)):
    # (Giữ nguyên code xử lý cũ của bạn)
    contents = await file.read()
    image = PIL.Image.open(io.BytesIO(contents))

    prompt = "Mô tả sản phẩm trong ảnh bằng 1 từ khóa tiếng Việt ngắn gọn..."
    try:
        response = model.generate_content([prompt, image])
        return {"keyword": response.text.strip()}
    except Exception as e:
        return {"keyword": "lỗi rồi", "error": str(e)}
