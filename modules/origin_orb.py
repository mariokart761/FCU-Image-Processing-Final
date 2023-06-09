import cv2
import numpy as np
import time

def origin_orb_detection(img, max_feature=30000, fastThreshold=20):
    # 初始化ORB偵測器
    orb = cv2.ORB_create(edgeThreshold=0)

    start_time = time.time() # detection timer start

    # 調整ORB特徵點偵測參數
    orb.setMaxFeatures(max_feature)
    orb.setFastThreshold(fastThreshold)

    # 初始化與原圖size相等的空白圖像
    img_with_keypoints = np.zeros_like(img)

    keypoints = orb.detect(img, None)
    end_time = time.time() # detection timer end

    # return data
    img_with_keypoints = cv2.drawKeypoints(img, keypoints, None, flags=0)
    keypoint_num = len(keypoints)
    detect_time = round(end_time - start_time, 3)
    
    return img_with_keypoints, keypoints, keypoint_num, detect_time

def origin_orb_comparison(img1, img2):
    img_with_keypoints1, full_keypoints1, keypoint_num1, t0 = origin_orb_detection(img1)
    img_with_keypoints2, full_keypoints2, keypoint_num2, t1 = origin_orb_detection(img2)
    
    h, w = img1.shape[:2]
    combined_img = np.zeros((h, w*2, 3), dtype=np.uint8)
    combined_img[:, :w] = img_with_keypoints1
    combined_img[:, w:] = img_with_keypoints2
    overlay = combined_img.copy()
    same_keypoints = []

    start_time = time.time() # comparison timer start

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
    
    end_time = time.time() # comparison timer end

    # 若兩張圖同個pixel都有檢測到keypoints，則繪製線段
    for kp in same_keypoints:
        x1, y1 = kp.pt
        x2, y2 = kp.pt
        x2 += w  # 將第二幅圖像中的特徵點的 x 坐標偏移 w 個像素，以match合成圖像中的位置
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
    comparison_time = round(end_time - start_time, 3) # 比對所花時間
    used_time = [t0, t1, comparison_time] # 偵測時間1, 偵測時間2, 比對時間

    return result_img, keypoint_data, used_time

# 先配置一張有特徵點的圖像並call函式improved_orb_detection，否則第一次執行OS未放入快取導致時間不準
def _first_call():
    _white_image = np.ones((200, 200, 1), dtype=np.uint8) * 255
    _black_image = np.zeros((100, 100, 1), dtype=np.uint8)
    _rows, _cols = _black_image.shape[:2]
    _roi = _white_image[-_rows:, -_cols:]
    _roi[:] = _black_image
    origin_orb_detection(_white_image)
_first_call()

# if __name__ == '__main__':
#     img_path1 = './img/testImg.png'
#     img_path2 = './img/brightFix-60.png'
#     _img1 = cv2.imread(img_path1, 0)
#     _img2 = cv2.imread(img_path2, 0)
#     result_img, keypoint_data, used_time = origin_orb_comparison(_img1, _img2)
    
#     # print data
#     print("----------")
#     print("Image 1:")
#     print("img_path1:" + img_path1[6:])
#     print("keypoint_num1:" + str(keypoint_data[0])) # 圖1的檢測到的特徵點數量
#     print("detect_time1:" + str(used_time[0]) + " s")
#     print(".")
#     print("Image 2:")
#     print("img_path2:" + img_path2[6:])
#     print("keypoint_num2:" + str(keypoint_data[1])) # 圖2的檢測到的特徵點數量
#     print("detect_time2:" + str(used_time[1]) + " s")
#     print(".")
#     print("matched_points:" + str(keypoint_data[2])) # 檢測到的相同特徵點數量
#     print("matched accuracy:" + str(round(keypoint_data[2]/keypoint_data[0]*100, 2)) + " %") # matched accuracy，圖2上檢測到幾%符合圖1的特徵點
#     print("match time:" + str(used_time[2]) + " s")
#     print("----------")
    
#     # cv2.imshow('Image with Keypoints1', result_img[0])
#     # cv2.imshow('Image with Keypoints2', result_img[1])
#     # cv2.imshow('Comparison Image', result_img[2])
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()