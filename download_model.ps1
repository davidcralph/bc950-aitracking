Write-Host "Downloading model files..."

(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/opencv/opencv_extra/4b5baee9ce6cad781f93b9ebbdca0749bd455a84/testdata/dnn/opencv_face_detector.pbtxt', 'opencv_face_detector.pbtxt')
(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/opencv/opencv_3rdparty/8033c2bc31b3256f0d461c919ecc01c2428ca03b/opencv_face_detector_uint8.pb', 'opencv_face_detector_uint8.pb')

Write-Host "Download Complete. Checking hashes..."

$pbtxt = Get-FileHash -Path opencv_face_detector.pbtxt -Algorithm SHA1
$pb = Get-FileHash -Path opencv_face_detector_uint8.pb -Algorithm SHA1

if ($pbtxt.Hash -eq "52f138a16f47bc56dbab0bbde9f12357f7682dc1" -and $pb.Hash -eq "4f2fdf6f231d759d7bbdb94353c5a68690f3d2ae") {
    Write-Host "Hashes Validated"
} else {
    Write-Host "Hashes Invalid. Please try again."
    Remove-Item opencv_face_detector.pbtxt
    Remove-Item opencv_face_detector_uint8.pb
}
