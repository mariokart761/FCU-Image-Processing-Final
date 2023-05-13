import cv2
import numpy as np

def origin_orb_detection(img_path, max_feature=30000, fastThreshold=20):
    img = cv2.imread(img_path, 0)

    # 初始化ORB偵測器
    orb = cv2.ORB_create(edgeThreshold=0)

    # 調整ORB特徵點偵測參數
    orb.setMaxFeatures(max_feature)
    orb.setFastThreshold(fastThreshold)

    # 初始化與原圖size相等的空白圖像
    img_with_keypoints = np.zeros_like(img)
    
    keypoints = orb.detect(img, None)
    img_with_keypoints = cv2.drawKeypoints(img, keypoints, None, flags=0)
    keypoint_num = len(keypoints)
    
    return img_with_keypoints, keypoints, keypoint_num

def improved_orb_comparison(img_path1, img_path2):
    img_with_keypoints1, full_keypoints1, keypoint_num1 = origin_orb_detection(img_path1)
    img_with_keypoints2, full_keypoints2, keypoint_num2 = origin_orb_detection(img_path2)
    
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