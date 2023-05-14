import cv2

def unsharp_mask_to_img(img, kernel_size = 3, sigma = 0, scale = 1):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 對圖像進行高斯濾波
    gaussian_img = cv2.GaussianBlur(gray_img, (kernel_size, kernel_size), sigma)

    # 原圖-濾波後的圖，得出 mask
    mask = cv2.subtract(gray_img, gaussian_img)

    # 銳化圖像 = 原圖 + (mask * scale)
    sharpen_img = cv2.add(gray_img, cv2.multiply(mask, scale))
    
    return sharpen_img, mask

# if __name__ == '__main__':
#     img_path = './img/testImg.png'
#     img = cv2.imread(img_path)
#     sharpen_img, mask = unsharp_mask_to_img(img)
#     cv2.imshow('Original Image', cv2.imread(img_path))
#     cv2.imshow('Unsharp Masking Image', sharpen_img)
#     cv2.imshow('Mask', mask)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()