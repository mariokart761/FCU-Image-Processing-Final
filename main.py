from fastapi import FastAPI, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import full_stack_orb_detection as orb_module
import numpy as np
import base64
import os
import cv2
import time

app = FastAPI()
app.mount("/static", StaticFiles(directory="dist"), name="static")

# 設定 CORS 中介軟體
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
       # 读取图像数据
        image_bytes = await img_content.read()

        # 进行图像处理
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        # 在这里进行适当的图像处理操作

        # 处理额外数据
        print("statusGaussianFilter:", statusGaussianFilter)
        print("statusBrightnessFixMethod:", statusBrightnessFixMethod)
        print("statusSharpen:", statusSharpen)
        print("statusAdaptiveThreshold:", statusAdaptiveThreshold)
        # "img_content":data["img_content"]要轉成np.ndarray
        config_data = {
            # "img_content":data["img_content"],
            "img_content":image,
            "statusGaussianFilter":statusGaussianFilter,
            "statusBrightnessFixMethod":statusBrightnessFixMethod,
            "statusSharpen":statusSharpen,
            "statusAdaptiveThreshold":statusAdaptiveThreshold
        }
        print(config_data)
        
        orbProcessor = orb_module.OrbProcessor()
        orbProcessor.setORBProcessor(config_data)
        result_img, keypoint_num, detect_time = orbProcessor.detectOrbFeature()
        print("Features : " + str(keypoint_num))
        print("Time : " + str(detect_time) + "s")
        
        # # 將接收到的圖片讀取為 OpenCV 的圖像格式
        # file_bytes = await image.read()
        # nparr = np.frombuffer(file_bytes, np.uint8)
        # cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # orbProcessor = orb_module.OrbProcessor()
        # orbProcessor.setORBProcessor(config_data)
        # result_img, keypoint_num, detect_time = orbProcessor.detectOrbFeature(cv_image)
        time.sleep(1)
        
        _, buffer = cv2.imencode('.jpg', result_img)
        image_str = base64.b64encode(buffer).decode('utf-8')
    except Exception as e:
        return {'error': str(e)}
        
    return JSONResponse(content={"processedImage": image_str})



rootPath = os.path.dirname(__file__)

if __name__ == '__main__':
    print(rootPath)
    os.system(f'python -m uvicorn main:app --port 8000 --reload')