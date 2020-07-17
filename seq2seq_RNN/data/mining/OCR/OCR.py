import numpy as np
import pytesseract
import cv2


def read_and_resize(file_path="Images/IMG_0506.png"):
    image = cv2.imread(file_path, 0)
    image = image[200:1800, 200:1042]
    return image


def enhance(src, loop_adjustment=True):
    a = 2.4
    a1 = 1.8
    a2 = 1.4
    b = -200
    b1 = -85
    b2 = -110
    i = 1
    while i > 0:
        image = cv2.convertScaleAbs(src, alpha=a, beta=b)
        if loop_adjustment:
            cv2.imshow("image1", cv2.resize(image, (384, 512)))
        k = cv2.waitKey(50)
        if k & 0xff == ord('a'):
            a += 0.01
            print(a, b)
            if a > 3:
                a = 3
        elif k & 0xff == ord('d'):
            a -= 0.01
            print(a, b)
            if a < 1:
                a = 1
        elif k & 0xff == ord('w'):
            b += 1
            print(a, b)
            if b > 255:
                b = 255
        elif k & 0xff == ord('s'):
            b -= 1
            print(a, b)
            if b < -255:
                b = -255
        elif k & 0xff == ord('q'):
            i -= 1
        if loop_adjustment:
            pass
        else:
            i -= 1

    i = 1
    while i > 0:
        image2 = cv2.convertScaleAbs(src, alpha=a1, beta=b1)
        if loop_adjustment:
            cv2.imshow("image2", cv2.resize(image2, (384, 512)))
        k = cv2.waitKey(50)
        if k & 0xff == ord('a'):
            a1 += 0.01
            print(a1, b1)
            if a1 > 3:
                a1 = 3
        elif k & 0xff == ord('d'):
            a1 -= 0.01
            print(a1, b1)
            if a1 < 1:
                a1 = 1
        elif k & 0xff == ord('w'):
            b1 += 1
            print(a1, b1)
            if b1 > 255:
                b1 = 255
        elif k & 0xff == ord('s'):
            b1 -= 1
            print(a1, b1)
            if b1 < -255:
                b1 = -255
        elif k & 0xff == ord('q'):
            i -= 1
        if loop_adjustment:
            pass
        else:
            i -= 1

    alpha = 0.5

    i = 1
    while i > 0:
        beta = 1 - alpha
        gamma = 0
        image3 = cv2.addWeighted(image, alpha, image2, beta, gamma)
        if loop_adjustment:
            cv2.imshow("image3", cv2.resize(image3, (384, 512)))
        k = cv2.waitKey(50)
        if k & 0xff == ord('a'):
            alpha += 0.01
            print(alpha, beta)
            if alpha > 1:
                alpha = 1
        elif k & 0xff == ord('d'):
            alpha -= 0.01
            print(alpha, beta)
            if alpha < 0:
                alpha = 0
        elif k & 0xff == ord('q'):
            i -= 1
        if loop_adjustment:
            pass
        else:
            i -= 1

    i = 1
    while i > 0:
        image4 = cv2.convertScaleAbs(image3, alpha=a2, beta=b2)
        if loop_adjustment:
            cv2.imshow("image3", cv2.resize(image4, (384, 512)))
        k = cv2.waitKey(50)
        if k & 0xff == ord('a'):
            a2 += 0.01
            print(a2, b2)
            if a2 > 3:
                a2 = 3
        elif k & 0xff == ord('d'):
            a2 -= 0.01
            print(a2, b2)
            if a2 < 1:
                a2 = 1
        elif k & 0xff == ord('w'):
            b2 += 1
            print(a2, b2)
            if b2 > 255:
                b2 = 255
        elif k & 0xff == ord('s'):
            b2 -= 1
            print(a2, b2)
            if b2 < -255:
                b2 = -255
        elif k & 0xff == ord('q'):
            i -= 1
        if loop_adjustment:
            pass
        else:
            i -= 1

    image = image4
    # kernel_sharpen_1 = np.array([
    #     [-1, -1, -1],
    #     [-1, 9, -1],
    #     [-1, -1, -1]])
    # image5 = cv2.filter2D(image4, -1, kernel_sharpen_1)
    # print("Sharpen")
    # cv2.imshow("image3", cv2.resize(image5, (384, 512)))
    # cv2.waitKey()
    return image


def binary_process(image):
    ret, thresh1 = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
    print("Binarize")
    cv2.imshow("image", cv2.resize(thresh1, (384, 512)))
    cv2.waitKey()
    kernel = np.ones((4, 4), np.uint8)
    thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
    print("Open")
    cv2.imshow("image", cv2.resize(thresh1, (384, 512)))
    cv2.waitKey()
    return thresh1


def recognizer(thresh):
    text = pytesseract.image_to_string(thresh, lang='chi_sim')

    print(text)


if __name__ == '__main__':
    resized = read_and_resize()
    enhanced = enhance(resized)
    recognizer(enhanced)
