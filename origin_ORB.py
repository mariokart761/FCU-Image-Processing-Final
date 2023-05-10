import cv2
import numpy as np

# 读取图像
img = cv2.imread('testImg.png')

# 初始化ORB检测器
orb = cv2.ORB_create(edgeThreshold=0)

# 调整ORB阈值参数
max_feature = 20000
orb.setMaxFeatures(max_feature)
orb.setFastThreshold(20)


# 将原始图像分割成5*5个子区域
m = 5
height, width, _ = img.shape
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
