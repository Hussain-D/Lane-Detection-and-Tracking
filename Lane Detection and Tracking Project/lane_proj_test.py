import cv2
import matplotlib.pyplot as plt
import numpy as np


# CONVERT INTO GREY SCALE IMAGE
def grey(image):
    image = np.asarray(image)
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


# GAUSSIAN BLUR TO REDUCE NOISE AND SMOOTHEN THE IMAGE
def gauss(image):
    return cv2.GaussianBlur(image, (5, 5), 0)


# CANNY EDGE DETECTION
def canny(image):
    edges = cv2.Canny(image, 200, 300)
    return edges


# IMPORTING IMAGE
img = cv2.imread("sample lane image.jpg")

# GREYSCALING
grey_img = grey(img)
# plt.imshow(grey_img)

# GAUSSIAN BLUR
gaussian_img = gauss(grey_img)
# plt.imshow(gaussian_img, cmap="gray")
# plt.title('Gaussian Blur'), plt.xticks([]), plt.yticks([])

# CANNY EDGE
canny_img = canny(gaussian_img)
# plt.imshow(canny_img, cmap="gray")
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

# TO HSV
hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
lower_yellow = np.array([20, 100, 100], dtype='uint8')
upper_yellow = np.array([30, 255, 255], dtype='uint8')

mask_yellow = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
mask_white = cv2.inRange(canny_img, 200, 255)
mask_yw = cv2.bitwise_or(mask_white, mask_yellow)
mask_yw_img = cv2.bitwise_and(canny_img, mask_yw)

plt.imshow(mask_yw_img, cmap="gray")
plt.title('mask_yw_img'), plt.xticks([]), plt.yticks([])
plt.show()