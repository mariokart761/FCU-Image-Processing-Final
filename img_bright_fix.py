import cv2

# 讀取圖像
def img_brightness_fix(img_path, brightness_fix = 60, write = False):
    img = cv2.imread(img_path)

    # 將亮度調整值轉換為亮度比例
    brightness_ratio = (100 + brightness_fix) / 100

    # 調整圖像亮度
    fixed_img = cv2.convertScaleAbs(img, alpha=brightness_ratio, beta=0)

    # 儲存調整後的圖像
    if (write): cv2.imwrite('./img/brightFix' + str(brightness_fix) + '.png', fixed_img)
    
    return fixed_img

# if __name__ == '__main__':
#     img_path = './img/testImg.png'
#     fixed_img = img_brightness_fix(img_path, brightness_fix = 90, write = True)
#     # 顯示調整後的圖像
#     cv2.imshow('Origin Image', cv2.imread(img_path))
#     cv2.imshow('Brightness Adjusted Image', fixed_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()