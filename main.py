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

# 設定 CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # 設定允許的來源（域名），設為 "*"則允許所有網域
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_html():
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/api/orbProcessing")
async def handle_request(img_content: UploadFile = File(...),
                         statusGaussianFilter: bool = Form(...),
                         statusBrightnessFixMethod: str = Form(...),
                         statusSharpen: bool = Form(...),
                         statusAdaptiveThreshold: bool = Form(...),
                         statusExperiment: str = Form(...),
                         statusBrightAdj: int = Form(...),):
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
        experiment = statusExperiment
        bright_adj = statusBrightAdj
        response_wait_time = 1 # server回應延遲
        
        orbProcessor = orb_module.OrbProcessor()
        orbProcessor.setORBProcessor(config_data)
        
        # exp1 論文實驗1：相比原始算法提升了多少
        if (experiment == "exp1"):
            result_img, keypoint_data, used_time = orbProcessor.compareToDefault()
            """
            result_img[0]: 左圖 detect結果圖
            result_img[1]: 右圖 detect結果圖
            result_img[2]: 兩圖 Matching結果圖
            keypoint_data[0]: 左圖檢測到的特徵點數量
            keypoint_data[1]: 右圖檢測到的特徵點數量
            keypoint_data[2]: Matching檢測到的相同特徵點數量
            used_time[0]: 左圖 detect時間
            used_time[1]: 右圖 detect時間
            used_time[2]: 兩圖 Matching時間
            Matching accuracy: round(keypoint_data[2]/keypoint_data[0]*100, 2) + "%"
            """
            # 不取matching結果
            _, buffer_left = cv2.imencode('.jpg', result_img[0])
            _, buffer_right = cv2.imencode('.jpg', result_img[1])
            image_str_left = base64.b64encode(buffer_left).decode('utf-8')
            image_str_right = base64.b64encode(buffer_right).decode('utf-8')
            content = {"processedImageLeft": image_str_left,
                    "processedImageRight": image_str_right,
                    "keypointNumLeft":keypoint_data[0],
                    "keypointNumRight":keypoint_data[1],
                    "detectTimeLeft":used_time[0],
                    "detectTimeRight":used_time[1],
                    }
            
            time.sleep(response_wait_time)
            
            return JSONResponse(content)
            ...
        # exp2 論文實驗2：調整輸入圖像的亮度，並查看特徵點比對數據
        elif (experiment == "exp2"):
            result_img, keypoint_data, used_time = orbProcessor.compareToDiffBrightness(brightness_adj = bright_adj)
            """
            result_img[0]: 左圖 detect結果圖
            result_img[1]: 右圖 detect結果圖
            result_img[2]: 兩圖 Matching結果圖
            keypoint_data[0]: 左圖檢測到的特徵點數量
            keypoint_data[1]: 右圖檢測到的特徵點數量
            keypoint_data[2]: Matching檢測到的相同特徵點數量
            used_time[0]: 左圖 detect時間
            used_time[1]: 右圖 detect時間
            used_time[2]: 兩圖 Matching時間
            Matching accuracy: round(keypoint_data[2]/keypoint_data[0]*100, 2) + "%"
            """            
            # 取matching結果
            _, buffer_left = cv2.imencode('.jpg', result_img[0])
            _, buffer_right = cv2.imencode('.jpg', result_img[1])
            _, buffer_match = cv2.imencode('.jpg', result_img[2])
            image_str_left = base64.b64encode(buffer_left).decode('utf-8')
            image_str_right = base64.b64encode(buffer_right).decode('utf-8')
            image_str_match = base64.b64encode(buffer_match).decode('utf-8')
            content = {"processedImageLeft": image_str_left,
                    "processedImageRight": image_str_right,
                    "processedImageMatch": image_str_match,
                    "keypointNumLeft":keypoint_data[0],
                    "keypointNumRight":keypoint_data[1],
                    "keypointNumMatch":keypoint_data[2],
                    "detectTimeLeft":used_time[0],
                    "detectTimeRight":used_time[1],
                    "detectTimeMatch":used_time[2],
                    "matchingAccuracy": round(keypoint_data[2]/keypoint_data[0]*100, 2)
                    }
            
            time.sleep(response_wait_time)
            
            return JSONResponse(content)
            ...
        
        # exp3 查看單張圖的效果
        elif (experiment == "exp3"):
            result_img, keypoint_num, detect_time = orbProcessor.detectOrbFeature()

            _, buffer = cv2.imencode('.jpg', result_img)
            image_str = base64.b64encode(buffer).decode('utf-8')
            content = {"processedImage": image_str,
                    "keypointNum":keypoint_num,
                    "detectTime":detect_time
                    }
            
            time.sleep(response_wait_time)
            
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