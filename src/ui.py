import cv2

class UI:
    def __init__(self, width):
        self.tool_y = 100
        self.colors = [
            (255, 255, 255),  
            (0, 0, 255),     
            (0, 255, 0),      
            (255, 0, 0),      
            (72, 85, 121),   
            (121, 85, 72)     
        ]
        self.brush_sizes = [10, 25, 40]
        self.width = width
        self.clear_button = (1100, 20, 1180, 80)  
        self.eraser_button = (1190, 20, 1270, 80) 
    def draw_toolbar(self, img, current_color, current_size):
        cv2.rectangle(img, (0, 0), (self.width, self.tool_y), (50, 50, 50), -1)

        for i, c in enumerate(self.colors):
            x = 20 + i * 100  
            cv2.rectangle(img, (x, 20), (x + 80, 80), c, -1)
            if c == current_color:
                cv2.rectangle(img, (x, 20), (x + 80, 80), (255, 255, 255), 3)

        for i, s in enumerate(self.brush_sizes):
            x = 620 + i * 80 
            cv2.circle(img, (x + 40, 50), s // 2, (255, 255, 255), -1)
            if s == current_size:
                cv2.circle(img, (x + 40, 50), s // 2 + 6, (0, 255, 0), 2)

        x1, y1, x2, y2 = self.eraser_button
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), -1)
        cv2.putText(img, "Silgi", (x1 + 5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        x1, y1, x2, y2 = self.clear_button
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 150), -1)
        cv2.putText(img, "CLEAR", (x1 + 5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    def check_toolbar_click(self, x, y, drawer):
        if y < self.tool_y:
            for i, c in enumerate(self.colors):
                cx = 20 + i * 100
                if cx < x < cx + 80:
                    drawer.draw_color = c

            for i, s in enumerate(self.brush_sizes):
                cx = 620 + i * 80
                if cx < x < cx + 80:
                    drawer.brush_thickness = s

            x1, y1, x2, y2 = self.eraser_button
            if x1 < x < x2 and y1 < y < y2:
                drawer.draw_color = (0, 0, 0)  

            x1, y1, x2, y2 = self.clear_button
            if x1 < x < x2 and y1 < y < y2:
                drawer.reset()