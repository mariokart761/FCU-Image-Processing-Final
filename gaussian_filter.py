import cv2

def gaussian_filter_to_img(img_path, kernel_size = 3, sigma = 0):
    img = cv2.imread(img_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussian_img = cv2.GaussianBlur(gray_img, (kernel_size, kernel_size), sigma)

    return gaussian_img

# if __name__ == '__main__':
#     img_path = './img/testImg.png'
#     gaussian_img = gaussian_filter_to_img(img_path)
#     cv2.imshow('Gaussian Image', gaussian_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

