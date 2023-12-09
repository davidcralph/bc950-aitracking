import cv2
import clr

print(r'./PTZDevice.dll')
clr.AddReference(r'./PTZDevice')

from PTZ import PTZDevice, PTZType
device = PTZDevice.GetDevice("BCC950 ConferenceCam", PTZType.Relative)

modelFile = "opencv_face_detector_uint8.pb"
configFile = "opencv_face_detector.pbtxt"
net = cv2.dnn.readNetFromTensorflow("opencv_face_detector_uint8.pb", "opencv_face_detector.pbtxt")

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            box = detections[0, 0, i, 3:7] * [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
            (x, y, x2, y2) = box.astype(int)
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)

            current_y = 0
            current_x = 0
                                    
            # move camera
            # get coords of box center and see how off we are
            x_center = (x + x2) / 2
            x_off_center = x_center - 320
            y_center = (y + y2) / 2
            y_off_center = y_center - 240
            
            # move camera
            if x_off_center > 100:
                if current_x != 20:
                    current_x += 1
                    device.Move(1, 0)
            elif x_off_center < -100:
                if current_x != -20:
                    current_x -= 1
                    device.Move(-1, 0)
                    
            if y_off_center < -80:
                if current_y != 5:
                    current_y += 1
                    device.Move(0, 1)
            elif y_off_center > 80:
                if current_y != -5:
                    current_y -= 1
                    device.Move(0, -1)
                 
            zoom_center = 200
            zoom_off_center = y2 - y - zoom_center
            
            if zoom_off_center > 80:
                device.Zoom(-1)
            elif zoom_off_center < -80:
                device.Zoom(1)
                            

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('Video', frame)

video_capture.release()
cv2.destroyAllWindows()
