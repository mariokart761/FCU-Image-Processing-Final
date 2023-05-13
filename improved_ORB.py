import cv2
import numpy as np

def best_orb_threshold(img, m):
    # 計算子區塊的大小
    height, width = img.shape[:2]
    block_size = int(min(height, width) / m)
    
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

def improved_orb_detection(img_path, m = 5):
    img = cv2.imread(img_path)
    gray_img = cv2.imread(img_path, 0)
    adaptive_threshold = best_orb_threshold(gray_img, m)

    # 初始化ORB偵測器
    orb = cv2.ORB_create(edgeThreshold=0)

    # 調整ORB特徵點偵測參數
    max_feature = 10000
    orb.setMaxFeatures(max_feature)

    # 將原始圖像分割為m*m塊
    height, width = img.shape[:2]
    block_width = width // m
    block_height = height // m

    # 初始化與原圖size相等的空白圖像
    img_with_keypoints = np.zeros_like(img)
    full_keypoints = []  # 新增的列表，用於存儲整張圖像的keypoints
    
    # 對每個子區域用不同的閾值進行ORB特徵點偵測
    for i in range(m):
        for j in range(m):
            # 獲取子區域座標
            x_start = i * block_width
            x_end = (i + 1) * block_width
            y_start = j * block_height
            y_end = (j + 1) * block_height
            
            # 提取子區域
            block = img[y_start:y_end, x_start:x_end]
            
            # 設置FastThreshold值
            orb.setFastThreshold(adaptive_threshold[i * 5 + j])
            
            # 子區域中偵測特徵點，並將座標對應至原始圖像
            keypoints = orb.detect(block, None)
            for kp in keypoints:
                kp.pt = (kp.pt[0] + x_start, kp.pt[1] + y_start)
            full_keypoints.extend(keypoints)
    # 繪製整張圖像的特徵點
    img_with_keypoints = cv2.drawKeypoints(img, full_keypoints, None, flags=0)
    
    keypoint_num = len(full_keypoints)
    
    return img_with_keypoints, full_keypoints, keypoint_num

def improved_orb_comparison(img_path1, img_path2):
    img_with_keypoints1, full_keypoints1, keypoint_num1 = improved_orb_detection(img_path1)
    img_with_keypoints2, full_keypoints2, keypoint_num2 = improved_orb_detection(img_path2)
    
    h, w, _ = cv2.imread(img_path1).shape
    combined_img = np.zeros((h, w*2, 3), dtype=np.uint8)
    combined_img[:, :w] = img_with_keypoints1
    combined_img[:, w:] = img_with_keypoints2
    overlay = combined_img.copy()
    same_keypoints = []

    # 建立 keypoints1 中每個特徵點的像素作為key，特徵點本身作為value的dict
    keypoints1_dict = {tuple(map(int, kp.pt)): kp for kp in full_keypoints1}

    # 檢查 keypoints2 中的特徵點是否有相同的像素
    for kp2 in full_keypoints2:
        x2, y2 = map(int, kp2.pt)
        pt2 = (x2, y2)
        
        # 檢查是否在 keypoints1_dict 中有相同的像素
        if pt2 in keypoints1_dict:
            # kp1 = keypoints1_dict[pt2]
            same_keypoints.append((kp2))
    
    # 若兩張圖同個pixel都有檢測到keypoints，則繪製線段
    for kp in same_keypoints:
        x1, y1 = kp.pt
        x2, y2 = kp.pt
        x2 += w  # 將第二個圖像中的特徵點的 x 坐標偏移 w 像素，以match合成圖像中的位置
        pt1 = (int(x1), int(y1))
        pt2 = (int(x2), int(y2))
        color = tuple(np.random.randint(0, 255, 3).tolist()) # 產生隨機顏色
        cv2.line(combined_img, pt1, pt2, color, 1)  # 繪製線段
    
    # cv2.line透明度設定，ref:https://gist.github.com/IAmSuyogJadhav/305bfd9a0605a4c096383408bee7fd5c
    alpha = 0.3  # Transparency factor.
    # Following line overlays transparent rectangle over the image
    comparison_img = cv2.addWeighted(overlay, alpha, combined_img, 1 - alpha, 0)
    
    # return data
    result_img = [img_with_keypoints1, img_with_keypoints2, comparison_img]
    matched_points = len(same_keypoints)
    keypoint_data = [keypoint_num1, keypoint_num2, matched_points]
    
    return result_img, keypoint_data

# if __name__ == '__main__':
#     img_path1 = './img/testImg.png'
#     img_path2 = './img/brightFix60.png'
#     result_img, keypoint_data = improved_orb_comparison(img_path1, img_path2)
    
#     # print data
#     print("----------")
#     print("Image 1:")
#     print("img_path1:" + img_path1[6:])
#     print("keypoint_num1:" + str(keypoint_data[0])) # 圖1的檢測到的特徵點數量
#     print(".")
#     print("Image 2:")
#     print("img_path2:" + img_path2[6:])
#     print("keypoint_num2:" + str(keypoint_data[1])) # 圖2的檢測到的特徵點數量
#     print(".")
#     print("matched_points:" + str(keypoint_data[2])) # 檢測到的相同特徵點數量
#     print("matched accuracy:" + str(round(keypoint_data[2]/keypoint_data[0]*100, 2)) + " %") # matched accuracy，圖2上檢測到幾%符合圖1的特徵點
#     print("----------")
    
#     cv2.imshow('Image with Keypoints1', result_img[0])
#     cv2.imshow('Image with Keypoints2', result_img[1])
#     cv2.imshow('Comparison Image', result_img[2])
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()