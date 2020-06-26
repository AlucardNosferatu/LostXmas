import numpy as np
import pytesseract
import cv2

image = cv2.imread("ocr_images/IMG_0505.png", 0)
print("Origin")
cv2.imshow("image", cv2.resize(image, (384, 512)))
cv2.waitKey()
image = image[200:1800, 200:1042]
image = cv2.convertScaleAbs(image, alpha=1.5, beta=-80)
print("Enhance Contrast")
cv2.imshow("image", cv2.resize(image, (384, 512)))
cv2.waitKey()
kernel_sharpen_1 = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]])
image = cv2.filter2D(image, -1, kernel_sharpen_1)
print("Sharpen")
cv2.imshow("image", cv2.resize(image, (384, 512)))
cv2.waitKey()
ret, thresh1 = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
print("Binarize")
cv2.imshow("image", cv2.resize(thresh1, (384, 512)))
cv2.waitKey()
kernel = np.ones((4, 4), np.uint8)
thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
print("Open")
cv2.imshow("image", cv2.resize(thresh1, (384, 512)))
cv2.waitKey()
text = pytesseract.image_to_string(thresh1, lang='chi_sim')
print(text)
