# bc950-aitracking
Low budget &amp; low quality AI face tracking for Logitech BC950 ConferenceCam

## Requirements
* OpenCV Face Detector pb and pbtxt
* Built copies of "PTZDevice.dll" and "DirectShowLib-2005.dll" from https://github.com/shanselman/Logitech-BCC950-PTZ-Lib

## Usage
Place the DLL and OpenCV files in the program directory and run ``tracker.py``. Be sure your ConferenceCam is in the **default** position else a lot of motor clicking will occur. I'm not responsible for any broken cameras!

## License
[MIT License](LICENSE)
