import cv2
from vidgear.gears import CamGear
import clr
import pyvirtualcam

print(r'./PTZDevice.dll')
clr.AddReference(r'./PTZDevice')

from PTZ import PTZDevice, PTZType
device = PTZDevice.GetDevice("BCC950 ConferenceCam", PTZType.Relative)

modelFile = "opencv_face_detector_uint8.pb"
configFile = "opencv_face_detector.pbtxt"

net = cv2.dnn.readNetFromTensorflow("opencv_face_detector_uint8.pb", "opencv_face_detector.pbtxt")

cv2.setUseOptimized(True)
cv2.setNumThreads(8)

if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    
screen_width = 1920
screen_height = 1080

video_capture = CamGear(source=0, backend=cv2.CAP_DSHOW, **{
    "CAP_PROP_FRAME_WIDTH": screen_width,
    "CAP_PROP_FRAME_HEIGHT": screen_height,
    "CAP_PROP_FPS": 30,
    "CAP_PROP_FOURCC": cv2.VideoWriter_fourcc(*"MJPG"),
    # backend
    }).start()

with pyvirtualcam.Camera(width=screen_width, height=screen_height, fps=30, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
  while True:
    frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            box = detections[0, 0, i, 3:7] * [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
            (x, y, x2, y2) = box.astype(int)
            #cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)

            current_y = 0
            current_x = 0
                                    
            # move camera
            # get coords of box center and see how off we are
            # ttodo: make this relative to the size of the screen
            x_center = (x + x2) / 2
            x_off_center = x_center - (screen_width / 2)
            y_center = (y + y2) / 2
            y_off_center = y_center - (screen_height / 2)
            
                        
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
                 
            # this is copilot junk maths it really needs replacing and sorting out
            square_size = (x2 - x) * (y2 - y)
            screen_size = screen_width * screen_height
            zoom_ratio = square_size / screen_size
            zoom_off_center = zoom_ratio - (1/3)
            
            if zoom_off_center > 0.1:
                device.Zoom(1)
            elif zoom_off_center < -0.1:
                device.Zoom(-1)
                            

    cam.send(frame)    

video_capture.stop()
cv2.destroyAllWindows()
