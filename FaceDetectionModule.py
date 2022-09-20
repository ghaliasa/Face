import cv2
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(
            self.minDetectionCon)

    def findFaces(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.results = self.faceDetection.process(imgRGB)
        bboxs = []

        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detection.score])
                img = self.fancyDraw(img, bbox)
                cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0],
                            bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (200, 100, 140), 2)

        return img, bboxs

    def fancyDraw(self, img, bbox, l=20, t=2, rt=1):
        x, y, w, h = bbox
        x1, y1 = x+w, y+h
        cv2.rectangle(img, bbox, (255, 0, 255), rt)
        # Top Left x,y
        cv2.line(img, (x, y), (x+l, y), (255, 0, 155), t)
        cv2.line(img, (x, y), (x, y+l), (255, 0, 155), t)
        # Top Right x 1,y
        cv2.line(img, (x1, y), (x1-l, y), (255, 0, 155), t)
        cv2.line(img, (x1, y), (x1, y+l), (255, 0, 155), t)
        # Bottom Left x,y
        cv2.line(img, (x, y1), (x+l, y1), (255, 0, 155), t)
        cv2.line(img, (x, y1), (x, y1-l), (255, 0, 155), t)
        # Bottom Right x 1,y
        cv2.line(img, (x1, y1), (x1-l, y1), (255, 0, 155), t)
        cv2.line(img, (x1, y1), (x1, y1-l), (255, 0, 155), t)
        return img


def main():
    cap = cv2.VideoCapture("FaceVideo/1.mp4")
    pTime = 0
    detector = FaceDetector()

    while True:
        success, img = cap.read()
        img, bboxs = detector.findFaces(img)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f'FPS:{int(fps)}', (20, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 45, 54), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
