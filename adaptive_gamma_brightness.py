import cv2
import numpy as np

# 以下為基於論文: 
# G. Cao, L. Huang, H. Tian, X. Huang, Y. Wang, and R. Zhi, 
# ‘‘Contrast enhancement of brightness-distorted images by improved adaptive gamma correction,’’
# Comput. Electr. Eng., vol. 66, pp. 569–582, Feb. 2018.
# 所提出的自適應gamma亮度校正的方法

def calculate_is_bright(img):
    isBright = True
    mean_gray = np.mean(img)
    if mean_gray < 128: isBright = False
    
    return isBright

def nagative_image(img):
    img = 255 - img
    
    return img

# 計算各灰度值出現機率
def calculate_grayscale_probabilities(image, precision=4):
    # 統計每個灰度值的出現次數
    grayscale_counts = np.zeros(256, dtype=int)
    unique, counts = np.unique(image, return_counts=True)
    grayscale_counts[unique] = counts
    
    # 計算每個灰度值的出現機率，取至小數點後 precision位數
    total_pixels = image.size
    grayscale_probabilities = np.round(grayscale_counts / total_pixels, precision)
    
    return grayscale_probabilities

# 將灰度值出現機率乘上權重
def apply_weighted_probabilities(probabilities, a=0.2):
    P_min = np.min(probabilities)
    P_max = np.max(probabilities)
    
    weighted_probabilities = (P_max * (probabilities - P_min) / (P_max - P_min)) ** a
    weighted_probabilities = np.round(weighted_probabilities, 4)
    
    return weighted_probabilities

# 計算gamma值
def calculate_gamma(weighted_probabilities, t=0.3):
    # cumulative_sum = np.sum(weighted_probabilities)
    sub_weighted_distribution = weighted_probabilities / np.sum(weighted_probabilities)
    weighted_distribution = np.cumsum(sub_weighted_distribution)
    gamma =  1 - weighted_distribution
    gamma[gamma < t] = t
    
    return gamma

# 計算套用gamma修正後的圖像，先得出t_mask，再用"原圖+beta*t_mask"得出亮度校正後的圖像
def modify_image_grayscale(image, gamma, beta=0.3):
    gamma_to_image = np.zeros_like(image, dtype=np.uint8)
    bright_fix_img = np.zeros_like(image, dtype=np.uint8)
    
    # 將gamma值直接套到原圖 (整體變暗)
    for i in range(256):
        gamma_to_image[image == i] = np.round(255 * (i * gamma[i] / 255))
    
    # t_mask = 原圖 - 套過gamma值的圖
    t_mask = image - gamma_to_image
    
    # 亮度校正後的圖像 =  原圖 + 權重beta * t_mask，權重預設為0.3
    bright_fix_img = np.round(image + beta * t_mask)
    
    # 圖像加法後灰度值可能會超過255，超過255的pixel截斷為255
    bright_fix_img[bright_fix_img > 255] = 255
    
    # 轉回 np.uint8型，否則輸出圖像會全白
    bright_fix_img = bright_fix_img.astype(np.uint8)
    
    return bright_fix_img

def adaptive_brightness_fix(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    isBright = calculate_is_bright(image)
    
    if(isBright):
        # 因為算法一定會讓圖像變白(圖像加法)，所以若平均灰度值>128時先做負片，再做亮度校正，最後再負片一次轉回來
        # 第一次負片
        temp_image = nagative_image(image)
        
        probabilities = calculate_grayscale_probabilities(temp_image)
        weighted_probabilities = apply_weighted_probabilities(probabilities)
        gamma = calculate_gamma(weighted_probabilities)
        bright_fix_img = modify_image_grayscale(temp_image, gamma)
        
        # 再做一次負片，以達到使高亮度圖像變暗的結果
        bright_fix_img = nagative_image(bright_fix_img)
    else:
        probabilities = calculate_grayscale_probabilities(image)
        weighted_probabilities = apply_weighted_probabilities(probabilities)
        gamma = calculate_gamma(weighted_probabilities)
        bright_fix_img = modify_image_grayscale(image, gamma)
        
    return bright_fix_img

# if __name__ == '__main__':
#     image_path = './img/testImg.png'
    
#     _bright_fix_img = adaptive_brightness_fix(image_path)
#     _image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     _isBright = calculate_is_bright(_image)
    
#     print('isBright:' +  f'{_isBright}')
#     print("原圖的平均灰度值:" + str(np.mean(_image)))
#     print("校正後平均灰度值:" + str(np.mean(_bright_fix_img)))
    
#     cv2.imshow('Origin Image', _image)
#     cv2.imshow('Modified Image', _bright_fix_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
