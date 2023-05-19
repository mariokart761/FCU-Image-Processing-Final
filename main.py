from fastapi import FastAPI, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import full_stack_orb_detection as orb_module
import numpy as np
import base64
import os
import cv2
import time

app = FastAPI()
app.mount("/static", StaticFiles(directory="dist"), name="static")

# 設定 CORS 中介
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # 設定允許的來源（域名），設為 "*"則允許所有網域
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_html():
    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/api/image")
async def handle_request(img_content: UploadFile = File(...),
                         statusGaussianFilter: bool = Form(...),
                         statusBrightnessFixMethod: str = Form(...),
                         statusSharpen: bool = Form(...),
                         statusAdaptiveThreshold: bool = Form(...),):
    try:
        image_bytes = await img_content.read()
        decode_image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

        config_data = {
            "img_content": decode_image,
            "statusGaussianFilter": statusGaussianFilter,
            "statusBrightnessFixMethod": statusBrightnessFixMethod,
            "statusSharpen": statusSharpen,
            "statusAdaptiveThreshold": statusAdaptiveThreshold
        }
        print(config_data)

        orbProcessor = orb_module.OrbProcessor()
        orbProcessor.setORBProcessor(config_data)
        result_img, keypoint_num, detect_time = orbProcessor.detectOrbFeature()
        print("Features : " + str(keypoint_num))
        print("Time : " + str(detect_time) + "s")

        _, buffer = cv2.imencode('.jpg', result_img)
        image_str = base64.b64encode(buffer).decode('utf-8')
        content = {"processedImage": image_str,
                   "keypointNum":keypoint_num,
                   "detectTime":detect_time
                }
        
        time.sleep(1)
        
        return JSONResponse(content)
    
    except Exception as e:
        return {'error': str(e)}

favicon_path = 'favicon.ico'
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

rootPath = os.path.dirname(__file__)

if __name__ == '__main__':
    os.system(f'python -m uvicorn main:app --port 8000 --reload')