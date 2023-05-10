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
    
    alpha = 0.3
    adaptive_orb_threshold = []
    for result in results:
        # 子區塊ORB閾值 = alpha * | 子區塊中心灰度值 - 子區塊灰度值變異數 |
        threshold = round(alpha*abs(result[1]-result[2]))
        if threshold < 7 : threshold = 7
        adaptive_orb_threshold.append(threshold)
    
    return adaptive_orb_threshold

# 读取图像
img = cv2.imread('testImg.png')
gray_img = cv2.imread('testImg.png', 0)
m = 5
adaptive_threshold = best_orb_threshold(gray_img, m)


# 初始化ORB检测器
orb = cv2.ORB_create(edgeThreshold=0)

# 调整ORB阈值参数
max_feature = 20000
orb.setMaxFeatures(max_feature)

# 将原始图像分割成m*m个子区域
height, width = img.shape[:2]
block_width = width // m
block_height = height // m

# 初始化一个与原始图像大小相同的空白图像
img_with_keypoints = np.zeros_like(img)
keypoint_num = 0
# 逐个子区域进行处理
for i in range(m):
    for j in range(m):
        # 获取子区域的坐标
        x_start = i * block_width
        x_end = (i + 1) * block_width
        y_start = j * block_height
        y_end = (j + 1) * block_height
        
        # 提取子区域
        block = img[y_start:y_end, x_start:x_end]
        
        # 设置FastThreshold值
        orb.setFastThreshold(adaptive_threshold[i * 5 + j])
        
        # 在子区域上检测特征点
        keypoints = orb.detect(block, None)
        keypoint_num += len(keypoints)
        # 在子区域上绘制特征点
        block_with_keypoints = cv2.drawKeypoints(block, keypoints, None, flags=0)
        
        # 将子区域的特征点图像贴回到完整图像上
        img_with_keypoints[y_start:y_end, x_start:x_end] = block_with_keypoints

print("FastThreshold:" + str(orb.getFastThreshold()))
print("MaxFeatures:" + str(orb.getMaxFeatures()))
print("ScoreType:" + str(orb.getScoreType()))
print("keypoint_num:" + str(keypoint_num))

cv2.imshow('Image with Keypoints', img_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()
