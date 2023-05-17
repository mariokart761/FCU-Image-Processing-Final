import cv2

def clahe_to_img(img, clipLimit=2.0, tileGridSize=(8,8)):
    
    # 創建CLAHE對象
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
    
    # 自適應直方圖均化
    clahe_img = clahe.apply(img)
    
    return clahe_img

# if __name__ == '__main__':
#     img_path = './img/testImg.png'
#     img = cv2.imread(img_path, 0)
#     clahe_img = clahe_to_img(img)
#     # 顯示結果
#     cv2.imshow('Original Image', img)
#     cv2.imshow('CLAHE Image', clahe_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
