# bc950-aitracking
Low budget &amp; low quality AI face tracking for Logitech BC950 ConferenceCam

## About
This project allows you to have the ConferenceCam follow your face when using it as a webcam.

## Requirements (for Building)
* MSBuild
* .NET Framework 4.x
* Python 3.10

## Installation (for Building)
1. Clone the repository
2. Run ``build_lib.bat`` to get a copy of the PTZ Library
3. Run ``download_model.ps1`` to get the OpenCV models
4. Install the requirements from ``requirements.txt``
5. See usage

## Usage
Run ``tracker.py``. Be sure your ConferenceCam is in the **default** position else a lot of motor clicking will occur. I'm not responsible for any broken cameras! You can reset your camera position by plugging it in again or with Logitech Camera Settings.

## Future Ideas
* Track body and other things
* Multiple face support
* Change movement speed/smoothing
* Preset movements for PTZ filming
* Ensure the camera is in the correct position when starting
* Linux support
* Code cleanup

## License
[MIT](LICENSE)
