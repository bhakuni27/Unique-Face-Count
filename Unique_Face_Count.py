# Import libraries
import cv2
import numpy as np
import face_recognition
import sys

# Checks the number of command line arguments and displays the correct usage
if len(sys.argv) != 2:
    print "USAGE:"
    print "Input from file  : python Unique_Face_Count.py <path of input file>"
    print "Input from webcam: python Unique_Face_Count.py webcam"
    sys.exit()

if sys.argv[1] == 'webcam':
    input_file = 0
else:
    input_file = sys.argv[1]

# Create a VideoCapture object and read from input file or webcam
cap = cv2.VideoCapture(input_file)

# Check if video opened successfully
if (cap.isOpened()== False):
    print("Error opening video file")

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

# Get fps of the input video
if int(major_ver)  < 3 :
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
else :
    fps = cap.get(cv2.CAP_PROP_FPS)

# Get default resolutions of the frame.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

if input_file != 0:
    # Define the codec and create VideoWriter object.The output is stored in 'output.mp4' file.
    out = cv2.VideoWriter('output.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width,frame_height))

# Initialize variables
known_faces = []
face_count = 0

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Find all the faces in the current frame of video using Histogram of Oriented Gradients model
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        # Every face in the current frame of video
        for top, right, bottom, left in face_locations:
            # Convert the face image to numpy array (which face_recognition.face_encodings uses)
            face_image = np.array(rgb_frame[top:bottom,left:right])
            try:
                face_encoding = face_recognition.face_encodings(face_image)[0]
            except:
                continue

            if len(known_faces) !=0:
                # See if the face is a match for the known face(s)
                match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.6)
                if not True in match:
                    face_count += 1
                    known_faces.append(face_encoding)
            else:
                face_count +=1
                known_faces.append(face_encoding)
                
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Display face count on the top-left corner of the frame
        cv2.putText(frame, "People Count = "+str(face_count), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        
        if input_file == 0:
            # Display the resulting frame"
            cv2.imshow('Video',frame)
            # Press q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            # Write the frame into the file 'output.mp4'
            out.write(frame)
        
    # Break the loop
    else:
        break

# Release the video capture object
cap.release()
if input_file != 0:
    out.release()

# Closes all the frames
cv2.destroyAllWindows()
