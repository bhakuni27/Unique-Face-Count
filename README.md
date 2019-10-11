# Unique Face Count

This is an example application to count the number of people appearing in a video frame. The input can be from a webcam or a video file. If the input is webcam, it displays the results in a new window frame in real time and if the input is a video file, then it creates another video file with the name as _**output.mp4**_ which reflects the results of the corresponding input video file.

## Prerequisites

Assuming you already have python and pip installed. Following are the dependencies:
+ opencv
```sh
pip install opencv-contrib-python
```
+ numpy
```sh
pip install numpy
```
+ face_recognition
```sh
pip install face_recognition
```
For installing face_recognition library you might need to install cmake `pip install cmake` and dlib `pip install dlib`.

## Usage

Use the following command to use webcam as input.
```sh
python Unique_Face_Count.py webcam
```
Use the following command to use a video file as input.
```sh
python Unique_Face_Count.py <path of the file>
```

## Limitations

+ Using only frontal faces for detection and recognition.
+ Doesn't work well in dark.