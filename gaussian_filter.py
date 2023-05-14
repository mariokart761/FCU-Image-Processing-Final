import cv2

def gaussian_filter_to_img(img, kernel_size = 3, sigma = 0):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussian_img = cv2.GaussianBlur(gray_img, (kernel_size, kernel_size), sigma)

    return gaussian_img

# if __name__ == '__main__':
#     img_path = './img/testImg.png'
#     img = cv2.imread(img_path)
#     gaussian_img = gaussian_filter_to_img(img)
#     cv2.imshow('Gaussian Image', gaussian_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

