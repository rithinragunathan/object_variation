import cv2
import numpy as np

def measurements(processed_frame,contours,frame):
    text = None
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 100:
            rect = cv2.minAreaRect(largest_contour)
            (x, y), (w, h), angle = rect
            box = cv2.boxPoints(rect)
            box = box.astype(int)

            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
            cv2.drawContours(frame, [box], 0, (255, 0, 0), 2)

            text = f"Area: {int(cv2.contourArea(largest_contour))} | Length: {int(h)} | Breadth: {int(w)}"

            cv2.putText(frame, text, (int(x), int(y) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    print(text)
    cv2.imshow("Webcam", frame)
    cv2.imshow("Processed", processed_frame)

def preprocessing(frame):
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    processed_frame = cv2.bilateralFilter(processed_frame, 9, 75, 75)
    processed_frame = cv2.Canny(processed_frame, 50, 150)
    _, processed_frame = cv2.threshold(processed_frame, 100, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(processed_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # measurement function call
    measurements(processed_frame,contours,frame)

def main():
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        raise RuntimeError("Camera is not accessible!")

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cv2.destroyAllWindows()
            raise RuntimeError("Can't read the video stream")
        
        '''    
        print(frame.size)
        break
        '''
        #preprocessing function call
        preprocessing(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
             break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
