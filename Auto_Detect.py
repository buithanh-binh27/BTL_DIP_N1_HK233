import cv2
import numpy as np
import GUI
import random
class AutoDetect:
    def __init__(self, image_path):
        self.pathImage = image_path
        self.heightImg = 640
        self.widthImg = 480
    def process_image(self):
        GUI.initializeTrackbars()
        img = cv2.imread(self.pathImage)

        while True:
            img = cv2.resize(img, (self.widthImg, self.heightImg))
            imgBlank = np.zeros((self.heightImg, self.widthImg, 3), np.uint8)
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 3)

            height, width = img.shape[:2]
            imgRectangle = cv2.rectangle(imgBlur.copy(), (0, 0), (width - 1, height - 1), (255, 255, 255), 2)

            thres = GUI.valTrackbars()
            imgThreshold = cv2.Canny(imgRectangle, thres[0], thres[1])
            kernel = np.ones((5, 5))
            imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)
            imgThreshold = cv2.erode(imgDial, kernel, iterations=1)

            imgContours = img.copy()
            imgBigContour = img.copy()
            contours, _ = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)

            for contour in contours:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                contour = cv2.approxPolyDP(contour, epsilon, True)
                color = [random.randint(0, 255) for _ in range(3)]
                cv2.drawContours(imgContours, [contour], -1, color, 2)

            biggest, maxArea = GUI.biggestContour(contours)
            if biggest.size != 0:
                biggest = GUI.reorder(biggest)
                cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)
                imgBigContour = GUI.drawRectangle(imgBigContour, biggest, 2)
                pts1 = np.float32(biggest)
                pts2 = np.float32([[0, 0], [self.widthImg, 0], [0, self.heightImg], [self.widthImg, self.heightImg]])
                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                imgWarpColored = cv2.warpPerspective(img, matrix, (self.widthImg, self.heightImg))

                imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
                imgWarpColored = cv2.resize(imgWarpColored, (self.widthImg, self.heightImg))

                imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
                imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
                imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
                imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 3)

                imageArray = ([img, imgThreshold],
                              [imgContours, imgBigContour])

            else:
                imageArray = ([img, imgThreshold],
                              [imgContours, imgBigContour])

            labels = [["Original", "Threshold", "Contours"],
                      ["Contours", "Biggest Contour"]]

            stackedImage = GUI.stackImages(imageArray, 0.75, labels)
            cv2.imshow("Result", stackedImage)

            if cv2.waitKey(0) & 0xFF == ord('s'):
                cv2.imshow('Auto_Detect', imgAdaptiveThre)
                cv2.waitKey(300)
                break

