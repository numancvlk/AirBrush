import cv2
import numpy as np

class DrawingUtils:
    def __init__(self, width, height):
        self.canvas = np.zeros((height, width, 3), np.uint8)
        self.xp, self.yp = 0, 0
        self.brush_thickness = 15
        self.eraser_thickness = 50
        self.draw_color = (0, 0, 255)

    def reset(self):
        self.canvas = np.zeros_like(self.canvas)

    def draw(self, x1, y1, color, eraser=False):
        if self.xp == 0 and self.yp == 0:
            self.xp, self.yp = x1, y1

        thickness = self.eraser_thickness if eraser else self.brush_thickness
        cv2.line(self.canvas, (self.xp, self.yp), (x1, y1), color, thickness)
        self.xp, self.yp = x1, y1

    def release(self):
        self.xp, self.yp = 0, 0

    def merge_with_frame(self, frame):
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
        inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, inv)
        frame = cv2.bitwise_or(frame, self.canvas)
        return frame
