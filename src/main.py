import cv2
from handtracker import HandTracker
from drawingutils import DrawingUtils
from ui import UI

def main():
    cap = cv2.VideoCapture(0)
    wCam, hCam = 1280, 720
    cap.set(3, wCam)
    cap.set(4, hCam)

    tracker = HandTracker()
    drawer = DrawingUtils(wCam, hCam)
    ui = UI(wCam)

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = tracker.detect_hands(rgb)

        ui.draw_toolbar(img, drawer.draw_color, drawer.brush_thickness)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lm_list = tracker.get_landmarks(handLms, img.shape)
                fingers = tracker.fingers_up(handLms)
                x1, y1 = lm_list[8] 
                x2, y2 = lm_list[12] 

                if y1 < ui.tool_y:
                    ui.check_toolbar_click(x1, y1, drawer)
                    drawer.release()
                    continue

                distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
                if fingers[1] == 1 and fingers[2] == 1 and distance < 80:
                    drawer.draw(x1, y1, drawer.draw_color, eraser=True)
                    cv2.circle(img, (x1, y1), 10, (0, 0, 0), -1)

                elif fingers[1] == 1 and fingers[2] == 0:
                    drawer.draw(x1, y1, drawer.draw_color, eraser=False)
                    cv2.circle(img, (x1, y1), 10, drawer.draw_color, -1)
                else:
                    drawer.release()

        img = drawer.merge_with_frame(img)
        cv2.imshow("BRUSH", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
