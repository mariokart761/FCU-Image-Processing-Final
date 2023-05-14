import os
import cv2
import numpy as np
import improved_orb
import origin_orb
import adaptive_gamma_brightness as gammaFix
from clahe import clahe_to_img
from gaussian_filter import gaussian_filter_to_img
from unsharp_masking import unsharp_mask_to_img
from img_bright_fix import brightness_fix_to_img

"""
# status_adaptive_threshold:
#   True : 使用 自適應ORB閾值
#   False : 不使用 自適應ORB閾值
#
# status_brightness_fix:
#   "None" : 不對圖像進行亮度校正
#   "Clahe" : 對圖像進行 自適應直方圖均化
#   "Adaptive Gamma" : 對圖像進行 Improved Adaptive Gamma Correction
# 
# status_gaussian_filter:
#   True : 使用 Gaussian Filter 去躁
#   False : 不使用 Gaussian Filter 去躁
#
# status_sharpen:
#   True : 使用 Unsharp Masking 進行銳化
#   False : 不進行銳化
"""

class OrbDetection:
    def __init__(self, 
                 img_path1 = "Not defined", 
                 img_path2 = "Not defined", 
                 statusAdaptiveThreshold = False, 
                 statusBrightnessFix = "None", 
                 statusGaussianFilter = False, 
                 statusSharpen = False):
        self.img_path1 = img_path1
        self.img_path2 = img_path2
        self.statusAdaptiveThreshold = statusAdaptiveThreshold
        self.statusBrightnessFix = statusBrightnessFix
        self.statusGaussianFilter = statusGaussianFilter
        self.statusSharpen = statusSharpen
    
    @property
    def img_path1(self):
        return self.img_path1
    
    @img_path1.setter
    def img_path1(self, value):
        if(type(value) == str):
            self.img_path1 = value
        else:
            raise ValueError("[INFO] img_path1 type 必須為 str")
    
    @property
    def img_path2(self):
        return self.img_path2
    
    @img_path2.setter
    def img_path2(self, value):
        if(type(value) == str):
            self.img_path2 = value
        else:
            raise ValueError("[INFO] img_path2 type 必須為 str")
    
    @property
    def statusAdaptiveThreshold(self):
        return self.statusAdaptiveThreshold
    
    @statusAdaptiveThreshold.setter
    def statusAdaptiveThreshold(self, value):
        if(value == True or value == False):
            self.statusAdaptiveThreshold = value
        else:
            raise ValueError("[INFO] statusAdaptiveThreshold的值必須為 True 或 False ")
    
    @property
    def statusBrightnessFix(self):
        return self.statusBrightnessFix
    
    @statusBrightnessFix.setter
    def statusBrightnessFix(self, value):
        if(value == True or value == False):
            self.statusBrightnessFix = value
        else:
            raise ValueError("[INFO] statusBrightnessFix的值必須為 \"None\" 或 \"Clahe\" 或 \"Adaptive Gamma\" ")
    
    @property
    def statusGaussianFilter(self):
        return self.statusGaussianFilter
    
    @statusGaussianFilter.setter
    def statusGaussianFilter(self, value):
        if(value == True or value == False):
            self.statusGaussianFilter = value
        else:
            raise ValueError("[INFO] statusGaussianFilter的值必須為 True 或 False ")
    
    @property
    def statusSharpen(self):
        return self.statusSharpen
    
    @statusSharpen.setter
    def statusSharpen(self, value):
        if(value == True or value == False):
            self.statusSharpen = value
        else:
            raise ValueError("[INFO] statusSharpen的值必須為 True 或 False ")
    
    # 檢查file path是否合法
    def checkImagePath(file_path):
        if(os.path.exists(file_path) == True):
            # 路徑存在
            try:
                _img = cv2.imread(file_path)
                if _img is not None:
                    print("[INFO] 成功讀取圖像: " + file_path)
                else:
                    print("[INFO] 非有效圖像: " + file_path)
            except Exception as e:
                # 發生其他異常
                print("[INFO] 讀取圖像時發生其它異常\n" + e)
            return
        else:
            # 路徑不存在
            raise FileNotFoundError("[INFO] 找不到指定路徑: " +  + file_path)
    
    # 依照status setting進行單圖像特徵點檢測
    def detectOrbFeature(self):
        self.checkImagePath(self.img_path1)
        _img = cv2.imread(self.img_path1)
        
        # 圖像增強環節
        # 高斯濾波
        if(self.statusGaussianFilter == True) : _img = gaussian_filter_to_img(_img)
        # 亮度校正
        if(self.statusBrightnessFix == "Clahe") : _img = clahe_to_img(_img)
        elif(self.statusBrightnessFix == "Adaptive Gamma") : gammaFix.adaptive_brightness_fix_to_img(_img)
        # unsharp masking
        if(self.statusSharpen == True): _img = unsharp_mask_to_img(_img)
        
        # 特徵點檢測環節
        # 使用自適應閾值檢測特徵點
        if(self.statusAdaptiveThreshold == True):
            
            ...
        # 使用固定閾值檢測特徵點
        elif(self.statusAdaptiveThreshold == False):
            
            ...
        ...
        

if __name__ == "__main__":
    ...