import cv2
import numpy as np

def best_orb_threshold(img, m):

    # 計算子區塊的大小
    height, width = img.shape[:2]
    block_size = int(min(height, width) / m)

    # 初始化結果列表
    results = []

    # 遍歷所有子區塊
    for i in range(m):
        for j in range(m):
            # 計算子區塊的左上角座標和右下角座標
            x1, y1 = j * block_size, i * block_size
            x2, y2 = x1 + block_size, y1 + block_size
            
            # 提取子區塊
            block = img[y1:y2, x1:x2]
            
            # 計算子區塊的灰度平均值、中心像素的灰度值、灰度值變異數
            mean = round(np.mean(block))
            center_pixel = block[block_size // 2, block_size // 2]
            
            best_t, thresh = cv2.threshold(block, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            
            
            # 將結果存入列表
            results.append((mean, int(center_pixel), int(best_t)))
    # print(results)
    
    alpha = 0.3
    adaptive_orb_threshold = []
    for result in results:
        # 子區塊ORB閾值 = alpha * | 子區塊中心灰度值 - 子區塊灰度值變異數 |
        threshold = round(alpha*abs(result[1]-result[2]))
        if threshold < 7 : threshold = 7
        adaptive_orb_threshold.append(threshold)
    # print(adaptive_orb_threshold)
    
    return adaptive_orb_threshold

if __name__ == '__main__':
    img = cv2.imread('testImg.png', 0)
    m=5
    adaptive_orb_threshold = best_orb_threshold(img, m)
    print(adaptive_orb_threshold)