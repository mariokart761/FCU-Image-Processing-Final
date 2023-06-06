import full_stack_orb_detection as orb_module
import matplotlib.pyplot as plt
import cv2


originORBProcessor = orb_module.OrbProcessor()
improvedORBProcessor = orb_module.OrbProcessor()

# orbProcessor data setting
filepath = './img/testImg.png'
image_content = cv2.imread(filepath)
originGaussianFilter = False
originBrightnessFixMethod = "None"
originSharpen = False
originAdaptiveThreshold = False
origin_config_data = {
    "img_content": image_content,
    "statusGaussianFilter": originGaussianFilter,
    "statusBrightnessFixMethod": originBrightnessFixMethod,
    "statusSharpen": originSharpen,
    "statusAdaptiveThreshold": originAdaptiveThreshold
}
improvedGaussianFilter = False
improvedBrightnessFixMethod = "Clahe"
improvedSharpen = True
improvedAdaptiveThreshold = True
improved_config_data = {
    "img_content": image_content,
    "statusGaussianFilter": improvedGaussianFilter,
    "statusBrightnessFixMethod": improvedBrightnessFixMethod,
    "statusSharpen": improvedSharpen,
    "statusAdaptiveThreshold": improvedAdaptiveThreshold
}
originORBProcessor.setORBProcessor(origin_config_data)
improvedORBProcessor.setORBProcessor(improved_config_data)

# 宣告plot需要用的資料list
origin_feature_points, improved_feature_points, origin_matching_accuracy = ([] for _ in range(3))
improved_matching_accuracy, origin_extraction_time, improved_extraction_time = ([] for _ in range(3))

# 計算不同亮度下的實驗數據，並記錄起來
MIN_BRIGHT = -90
MAX_BRIGHT = 90
for bright_adj in range(MIN_BRIGHT, MAX_BRIGHT+1):
    _, origin_keypoint_data, origin_used_time = originORBProcessor.compareToDiffBrightness(brightness_adj = bright_adj)
    _, improved_keypoint_data, improved_used_time = improvedORBProcessor.compareToDiffBrightness(brightness_adj = bright_adj)
    
    origin_feature_points.append(origin_keypoint_data[1])
    origin_matching_accuracy.append(round(origin_keypoint_data[2]/origin_keypoint_data[0]*100, 2))
    origin_extraction_time.append(origin_used_time[1]*1000)
    
    improved_feature_points.append(improved_keypoint_data[1])
    improved_matching_accuracy.append(round(improved_keypoint_data[2]/improved_keypoint_data[0]*100, 2))
    improved_extraction_time.append(improved_used_time[1]*1000)
    print(f"[INFO] Brightness {bright_adj} complete")
    

# Number of feature points 資料可視化
x = list(range(MIN_BRIGHT, MAX_BRIGHT+1))
y1 = origin_feature_points
y2 = improved_feature_points
plt.plot(x, y1, label='Origin ORB')
plt.plot(x, y2, label='Improved ORB')
plt.xlabel('Brightness increase (%)')  # x 軸標籤
plt.ylabel('Number of feature points')  # y 軸標籤
# plt.xlim(MIN_BRIGHT, MAX_BRIGHT+1)  # x 軸範圍
plt.ylim(0, max([max(origin_feature_points),max(improved_feature_points)])*1.3)  # y 軸範圍
plt.legend()  # 顯示圖
plt.title('Number of feature points comparison')  # 圖標題
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(20)) # 調整 x 軸間距為20
# plt.grid(True)  # 顯示格線
plt.show()

# Matching accuracy 資料可視化
x = list(range(MIN_BRIGHT, MAX_BRIGHT+1))
y1 = origin_matching_accuracy
y2 = improved_matching_accuracy
plt.plot(x, y1, label='Origin ORB')
plt.plot(x, y2, label='Improved ORB')
plt.xlabel('Brightness increase (%)')  # x 軸標籤
plt.ylabel('Matching accuracy (%)')  # y 軸標籤
# plt.xlim(MIN_BRIGHT, MAX_BRIGHT+1)  # x 軸範圍
plt.ylim(0, 100+20)  # y 軸範圍
plt.legend()  # 顯示圖
plt.title('Matching accuracy comparison')  # 圖標題
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(20)) # 調整 x 軸間距為20
# plt.grid(True)  # 顯示格線
plt.show()

# Extract time 資料可視化
x = list(range(MIN_BRIGHT, MAX_BRIGHT+1))
y1 = origin_extraction_time
y2 = improved_extraction_time 
plt.plot(x, y1, label='Origin ORB')
plt.plot(x, y2, label='Improved ORB')
plt.xlabel('Brightness increase (%)')  # x 軸標籤
plt.ylabel('Extract time (ms)')  # y 軸標籤
# plt.xlim(MIN_BRIGHT, MAX_BRIGHT+1)  # x 軸範圍
plt.ylim(0, max([max(origin_extraction_time),max(improved_extraction_time)])*3)  # y 軸範圍
plt.legend()  # 顯示圖
plt.title('Extract time comparison')  # 圖標題
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(20)) # 調整 x 軸間距為20
# plt.grid(True)  # 顯示格線
plt.show()
