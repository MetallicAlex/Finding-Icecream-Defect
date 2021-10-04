import cv2
import numpy as np
from datetime import datetime
import time

from fid import System


class PackageDetector:
    image = None
    system = System()
    roi = None

    def detect(self, img, roi=None):
        start_time = datetime.now()
        self.roi = roi
        self.image = img
        self.image = cv2.medianBlur(self.image, 3)
        self.image = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 131, -4)
        self.image = cv2.erode(self.image, np.ones((3, 3)))
        self.image = cv2.dilate(self.image, np.ones((3, 3)))
        cv2.imshow('Mask', self.image)
        contours, hierarchy = cv2.findContours(self.image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = filter(lambda x: cv2.contourArea(x) > 800, contours)
        contours = list(reversed(sorted(contours, key=lambda x: cv2.contourArea(x))))
        best_x = None
        best_y = None
        best_h = None
        best_w = None
        best_box = None
        best_c = None
        for contour in contours:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            image, size, center = self.rotate_feature(rect)
            if self.filter_circle(image):
                if 50 < size[0] < 130:
                    if best_x is None:
                        best_x, best_y, best_w, best_h, best_box, best_c = rect[0][0], rect[0][1], size[0], size[
                            1], box, center
                    elif best_y > rect[0][1]:
                        best_x, best_y, best_w, best_h, best_box, best_c = rect[0][0], rect[0][1], size[0], size[
                            1], box, center
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if best_x:
            if roi:
                flag = self.is_defect(best_x, best_y)
                self.system.save_image(img, start_time, flag)
                print(flag, best_x, best_y)
            cv2.drawContours(img, [best_box], 0, (0, 255, 0), 3)
            cv2.circle(img, (int(best_c[0]), int(best_c[1])), 2, (0, 255, 0), 3)
            # if flag:
            #     self.system.send_signal_to_controller(4, flag, 1)
            #     time.sleep(0.02)
            #     self.system.send_signal_to_controller(4, 0, 1)
        return img

    def rotate_feature(self, rect):
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        W = rect[1][0]
        H = rect[1][1]

        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        x2 = max(Xs)
        y1 = min(Ys)
        y2 = max(Ys)

        angle = rect[2]
        if angle < -45:
            angle += 90
        elif angle > 45:
            angle -= 90

        center = ((x1 + x2) / 2, (y1 + y2) / 2)
        size = (x2 - x1, y2 - y1)
        M = cv2.getRotationMatrix2D((size[0] / 2, size[1] / 2), angle, 1.0)
        cropped = cv2.getRectSubPix(self.image, size, center)
        cropped = cv2.warpAffine(cropped, M, size)
        croppedW = H if H > W else W
        croppedH = H if H < W else W
        croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW), int(croppedH)), (size[0] / 2, size[1] / 2))
        return croppedRotated, size, center

    def filter_circle(self, roi, pos=None):
        h, w = roi.shape[:2]
        left = roi[int(0.3 * h):int(0.7 * h), :int(0.3 * w)]
        right = roi[int(0.3 * h):int(0.7 * h), int(0.7 * w):]
        top = roi[:int(0.3 * h), int(0.3 * w):int(0.7 * w)]
        bottom = roi[int(0.7 * h):, int(0.3 * w):int(0.7 * w)]
        center = roi[int(0.3 * h):int(0.7 * h), int(0.3 * w):int(0.7 * w)]
        center = cv2.countNonZero(center) / (center.shape[0] * center.shape[1])
        left = cv2.countNonZero(left) / (left.shape[0] * left.shape[1])
        #     print(left, center)
        #     right = cv2.countNonZero(right)/(right.shape[0]*right.shape[1])
        #     top = cv2.countNonZero(top)/(top.shape[0]*top.shape[1])
        #     bottom = cv2.countNonZero(bottom)/(bottom.shape[0]*bottom.shape[1])
        if left >= 0.3 and center <= 0.45:
            return True
        return False

    def is_defect(self, x, y):
        if self.roi.y0 <= y <= self.roi.y1:
            return False
        else:
            return True
