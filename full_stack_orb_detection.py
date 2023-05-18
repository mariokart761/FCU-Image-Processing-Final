import os
import cv2
import numpy as np
import modules.improved_orb as improved_orb
import modules.origin_orb as origin_orb
import modules.adaptive_gamma_brightness as gammaFix
from modules.clahe import clahe_to_img
from modules.gaussian_filter import gaussian_filter_to_img
from modules.unsharp_masking import unsharp_mask_to_img
from modules.img_bright_fix import brightness_fix_to_img

"""
# status_adaptive_threshold:
#   True : 使用 自適應ORB閾值
#   False : 不使用 自適應ORB閾值
#
# status_brightness_fix:
#   "None" : 不對圖像進行亮度校正
#   "Clahe" : 對圖像進行 自適應直方圖均化
#   "Adaptive_Gamma" : 對圖像進行 Improved Adaptive_Gamma Correction
# 
# status_gaussian_filter:
#   True : 使用 Gaussian Filter 去躁
#   False : 不使用 Gaussian Filter 去躁
#
# status_sharpen:
#   True : 使用 Unsharp Masking 進行銳化
#   False : 不進行銳化
"""

class OrbProcessor:
    def __init__(self, 
                 img_path = "Not defined.", 
                 statusAdaptiveThreshold = False, 
                 statusBrightnessFixMethod = "None", 
                 statusGaussianFilter = False, 
                 statusSharpen = False):
        self._img_path = img_path
        self._statusAdaptiveThreshold = statusAdaptiveThreshold
        self._statusBrightnessFixMethod = statusBrightnessFixMethod
        self._statusGaussianFilter = statusGaussianFilter
        self._statusSharpen = statusSharpen
    
    @property
    def img_path(self):
        return self._img_path
    
    @img_path.setter
    def img_path(self, value):
        if(type(value) == str):
            self._img_path = value
        else:
            raise ValueError("[INFO] img_path type 必須為 str")
    
    @property
    def statusAdaptiveThreshold(self):
        return self._statusAdaptiveThreshold
    
    @statusAdaptiveThreshold.setter
    def statusAdaptiveThreshold(self, value):
        if(value == True or value == False):
            self._statusAdaptiveThreshold = value
        else:
            raise ValueError("[INFO] statusAdaptiveThreshold的值必須為 True 或 False ")
    
    @property
    def statusBrightnessFixMethod(self):
        return self._statusBrightnessFixMethod
    
    @statusBrightnessFixMethod.setter
    def statusBrightnessFixMethod(self, value):
        if(value == "None" or value == "Clahe" or value == "Adaptive_Gamma"):
            self._statusBrightnessFixMethod = value
        else:
            raise ValueError("[INFO] statusBrightnessFixMethod的值必須為 \"None\" 或 \"Clahe\" 或 \"Adaptive_Gamma\" ")
    
    @property
    def statusGaussianFilter(self):
        return self._statusGaussianFilter
    
    @statusGaussianFilter.setter
    def statusGaussianFilter(self, value):
        if(value == True or value == False):
            self._statusGaussianFilter = value
        else:
            raise ValueError("[INFO] statusGaussianFilter的值必須為 True 或 False ")
    
    @property
    def statusSharpen(self):
        return self._statusSharpen
    
    @statusSharpen.setter
    def statusSharpen(self, value):
        if(value == True or value == False):
            self._statusSharpen = value
        else:
            raise ValueError("[INFO] statusSharpen的值必須為 True 或 False ")
    
    # 檢查file path是否合法
    def checkImagePath(self):
        if(os.path.exists(self.img_path) == True):
            # 路徑存在
            try:
                _img = cv2.imread(self.img_path)
                if _img is not None:
                    # print("[INFO] 成功讀取圖像: " + self.img_path)
                    return
                else:
                    print("[INFO] 非有效圖像: " + self.img_path)
                    return
            except Exception as e:
                # 發生其他異常
                print("[INFO] 讀取圖像時發生其它異常\n" + e)
        else:
            # 路徑不存在
            raise FileNotFoundError("[INFO] 找不到指定路徑: " + self.img_path)
        
        return
    
    # 依照status setting進行單圖像特徵點檢測
    def detectOrbFeature(self):
        self.checkImagePath()
        _img = cv2.imread(self.img_path, 0)
        
        # 圖像增強環節
        # 高斯濾波
        if(self.statusGaussianFilter == True) : _img = gaussian_filter_to_img(_img)
        # 亮度校正
        if(self.statusBrightnessFixMethod == "Clahe") : _img = clahe_to_img(_img)
        elif(self.statusBrightnessFixMethod == "Adaptive_Gamma") : _img = gammaFix.adaptive_brightness_fix_to_img(_img)
        # unsharp masking
        if(self.statusSharpen == True): _img, mask  = unsharp_mask_to_img(_img)
        
        # 特徵點檢測環節
        # 使用自適應閾值檢測特徵點
        if(self.statusAdaptiveThreshold == True):
            result_img, keypoints, keypoint_num, detect_time = improved_orb.improved_orb_detection(_img)
        # 使用固定閾值檢測特徵點
        elif(self.statusAdaptiveThreshold == False):
            result_img, keypoints, keypoint_num, detect_time = origin_orb.origin_orb_detection(_img)
        
        return result_img, keypoint_num, detect_time
    
    def compareToDefault(self):
        # 左圖顯示未經圖像增強的結果，右圖顯示依照Setting進行圖像增強的結果
        self.checkImagePath()
        _img1 = cv2.imread(self.img_path, 0)
        _img2 = cv2.imread(self.img_path, 0)
        
        # 圖像增強環節
        # 高斯濾波
        if(self.statusGaussianFilter == True) : _img2 = gaussian_filter_to_img(_img2)
        # 亮度校正
        if(self.statusBrightnessFixMethod == "Clahe") : _img2 = clahe_to_img(_img2)
        elif(self.statusBrightnessFixMethod == "Adaptive_Gamma") : _img2 = gammaFix.adaptive_brightness_fix_to_img(_img2)
        # unsharp masking
        if(self.statusSharpen == True): _img2, mask  = unsharp_mask_to_img(_img2)
        
        # 特徵點檢測環節
        # 使用自適應閾值檢測特徵點
        if(self.statusAdaptiveThreshold == True):
            result_img, keypoint_data, used_time = improved_orb.improved_orb_comparison(_img1, _img2)
        # 使用固定閾值檢測特徵點
        elif(self.statusAdaptiveThreshold == False):
            result_img, keypoint_data, used_time = origin_orb.origin_orb_comparison(_img1, _img2)
        
        return result_img, keypoint_data, used_time
    
    def compareToDiffBrightness(self, brightness_adj = 60):
        # 左圖依照Setting變動的算法結果，右圖顯示依照Setting變動的算法套用在不同亮度的結果
        self.checkImagePath()
        _img1 = cv2.imread(self.img_path, 0)
        _img2 = brightness_fix_to_img(_img1, brightness_fix = brightness_adj)
        
        # 圖像增強環節
        # 高斯濾波
        if(self.statusGaussianFilter == True) : 
            _img1 = gaussian_filter_to_img(_img1)
            _img2 = gaussian_filter_to_img(_img2)
        # 亮度校正
        if(self.statusBrightnessFixMethod == "Clahe") :
            _img1 = clahe_to_img(_img1)
            _img2 = clahe_to_img(_img2)
        elif(self.statusBrightnessFixMethod == "Adaptive_Gamma") : 
            _img1 = gammaFix.adaptive_brightness_fix_to_img(_img1)
            _img2 = gammaFix.adaptive_brightness_fix_to_img(_img2)
        # unsharp masking
        if(self.statusSharpen == True):
            _img1, mask = unsharp_mask_to_img(_img1)
            _img2, mask = unsharp_mask_to_img(_img2)
        
        # 特徵點檢測環節
        # 使用自適應閾值檢測特徵點
        if(self.statusAdaptiveThreshold == True):
            result_img, keypoint_data, used_time = improved_orb.improved_orb_comparison(_img1, _img2)
        # 使用固定閾值檢測特徵點
        elif(self.statusAdaptiveThreshold == False):
            result_img, keypoint_data, used_time = origin_orb.origin_orb_comparison(_img1, _img2)
        
        return result_img, keypoint_data, used_time

    def setORBProcessor(self, setting_data):
        self.img_path = setting_data["img_path"]
        self.statusGaussianFilter = setting_data["statusGaussianFilter"]
        self.statusBrightnessFixMethod = setting_data["statusBrightnessFixMethod"]
        self.statusSharpen = setting_data["statusSharpen"]
        self.statusAdaptiveThreshold = setting_data["statusAdaptiveThreshold"]
    
    

if __name__ == "__main__":
    # orbProcessor setting data
    filepath = './img/testImg.png'
    statusGaussianFilter = False
    statusBrightnessFixMethod = "Clahe"
    statusSharpen = True
    statusAdaptiveThreshold = True
    
    # set orbProcessor
    orbProcessor = OrbProcessor()
    orbProcessor.img_path = filepath
    orbProcessor.statusGaussianFilter = statusGaussianFilter
    orbProcessor.statusBrightnessFixMethod = statusBrightnessFixMethod
    orbProcessor.statusSharpen = statusSharpen
    orbProcessor.statusAdaptiveThreshold = statusAdaptiveThreshold
    
#     # 顯示 orbProcessor setting
#     print("----------")
#     print("img_path : " + orbProcessor.img_path)
#     print("statusGaussianFilter : " + str(orbProcessor.statusGaussianFilter))
#     print("statusBrightnessFixMethod : "+ str(orbProcessor.statusBrightnessFixMethod))
#     print("statusSharpen : "+ str(orbProcessor.statusSharpen))
#     print("statusAdaptiveThreshold : "+ str(orbProcessor.statusAdaptiveThreshold))
    
#     # check result - detectOrbFeature
#     result_img1, keypoint_num, detect_time = orbProcessor.detectOrbFeature()
#     print("----------")
#     print("detectOrbFeature:")
#     print("Keypoint counts: " + str(keypoint_num))
#     print("Detect time:" + str(detect_time) + "s")
    
#     # check result - compareToDefault
#     result_img2, keypoint_data2, used_time2 = orbProcessor.compareToDefault()
#     print("----------")
#     print("compareToDefault:")
#     print("Keypoint counts 1 : " + str(keypoint_data2[0])) # 左圖的檢測到的特徵點數量
#     print("Detect time 1 : " + str(used_time2[0]) + " s")
#     print("Keypoint counts 2 : " + str(keypoint_data2[1])) # 右圖的檢測到的特徵點數量
#     print("Detect time 2 : " + str(used_time2[1]) + " s")
#     print("Matching points : " + str(keypoint_data2[2])) # 檢測到的相同特徵點數量
#     print("Matching accuracy : " + str(round(keypoint_data2[2]/keypoint_data2[0]*100, 2)) + " %") # 右圖上檢測到幾%符合左圖的特徵點
#     print("Matching time : " + str(used_time2[2]) + " s")
    
#     # check result - compareToDiffBrightness
#     adj = -60
#     result_img3, keypoint_data3, used_time3 = orbProcessor.compareToDiffBrightness(brightness_adj = adj)
#     print("----------")
#     print("compareToDiffBrightness:")
#     print("Keypoint counts 1 : " + str(keypoint_data3[0])) # 左圖的檢測到的特徵點數量
#     print("Detect time 1 : " + str(used_time3[0]) + " s")
#     print("Keypoint counts 2 : " + str(keypoint_data3[1])) # 右圖的檢測到的特徵點數量
#     print("Detect time 2 : " + str(used_time3[1]) + " s")
#     print("Matching points : " + str(keypoint_data3[2])) # 檢測到的相同特徵點數量
#     print("Matching accuracy : " + str(round(keypoint_data3[2]/keypoint_data3[0]*100, 2)) + " %") # 右圖上檢測到幾%符合左圖的特徵點
#     print("Matching time : " + str(used_time3[2]) + " s")
#     print("----------")
    
#     # cv2.imshow("Result - detectOrbFeature", result_img1)
#     # cv2.imshow("Result - compareToDefault left", result_img2[0])
#     # cv2.imshow("Result - compareToDefault right", result_img2[1])
#     # cv2.imshow("Result - compareToDefault mix", result_img2[2])
#     # cv2.imshow("Result - compareToDiffBrightness left", result_img3[0])
#     # cv2.imshow("Result - compareToDiffBrightness right", result_img3[1])
#     # cv2.imshow("Result - compareToDiffBrightness mix", result_img3[2])
    
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()