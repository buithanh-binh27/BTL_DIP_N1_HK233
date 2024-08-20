import cv2
import numpy as np

class ManualDetect:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.points = []
        self.selected_point = None
        self.dragging = False
        self.window_name = 'Adjust Rectangle'

    def apply_clahe(self, image, clip_limit=2.0, tile_grid_size=(16, 16)):
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        return clahe.apply(image)

    def draw_rectangle(self, image, pts):
        temp_image = image.copy()
        cv2.polylines(temp_image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        return temp_image

    def window_popup(self, title, image):
        cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
        screen_res = 1920, 1080
        scale_width = screen_res[0] / image.shape[1]
        scale_height = screen_res[1] / image.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(image.shape[1] * scale)
        window_height = int(image.shape[0] * scale)
        cv2.resizeWindow(title, window_width, window_height)
        cv2.imshow(title, image)

    def mouse_handler(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, pt in enumerate(self.points):
                if np.linalg.norm(pt - np.array([x, y])) < 10:
                    self.selected_point = i
                    self.dragging = True
                    break

        elif event == cv2.EVENT_MOUSEMOVE and self.dragging:
            if self.selected_point is not None:
                x = max(0, min(x, self.image.shape[1] - 1))
                y = max(0, min(y, self.image.shape[0] - 1))
                self.points[self.selected_point] = np.array([x, y])
                temp_image = self.draw_rectangle(self.image, np.array(self.points))
                cv2.imshow(self.window_name, temp_image)

        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False
            self.selected_point = None

    def scan(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpen = cv2.GaussianBlur(gray, (0, 0), 3)
        sharpen = cv2.addWeighted(gray, 1.5, sharpen, -0.5, 0)
        thresh = cv2.adaptiveThreshold(sharpen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 15)
        return thresh

    def process_image(self):
        h, w = self.image.shape[:2]
        self.points = [np.array([int(w * 0.2), int(h * 0.2)]), np.array([int(w * 0.8), int(h * 0.2)]),
                       np.array([int(w * 0.8), int(h * 0.8)]), np.array([int(w * 0.2), int(h * 0.8)])]

        img_with_rect = self.draw_rectangle(self.image, np.array(self.points))
        self.window_popup(self.window_name, img_with_rect)
        cv2.setMouseCallback(self.window_name, self.mouse_handler)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                break

        if len(self.points) == 4:
            dst_points = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype="float32")
            M = cv2.getPerspectiveTransform(np.array(self.points, dtype="float32"), dst_points)
            warped = cv2.warpPerspective(self.image, M, (w, h))
            self.window_popup('Warped', self.scan(warped))
            cv2.waitKey(0)

        cv2.destroyAllWindows()
