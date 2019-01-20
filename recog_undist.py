import face_recognition
import cv2
import os
import urllib.request
import numpy as np
import clever_cam_calibration.clevercamcalib as ccc

faces_images=[]
for i in os.listdir('faces/'):
    faces_images.append(face_recognition.load_image_file('faces/'+i))
known_face_encodings=[]
for i in faces_images:
    known_face_encodings.append(face_recognition.face_encodings(i)[0])
known_face_names=[]
for i in os.listdir('faces/'):
    i=i.split('.')[0]
    known_face_names.append(i)


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    req = urllib.request.urlopen('http://192.168.11.1:8080/snapshot?topic=/main_camera/image_raw')
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    frame = cv2.imdecode(arr, -1)
    height_or, width_or, depth_or = frame.shape
    if height_or==240 and width_or==320:
        frame=ccc.get_undistorted_image(frame,ccc.CLEVER_FISHEYE_CAM_320)
    elif height_or==480 and width_or==640:
        frame=ccc.get_undistorted_image(frame,ccc.CLEVER_FISHEYE_CAM_640)
    else:
        frame=ccc.get_undistorted_image(frame,input("Input your path to the .yaml file: "))
    height_unz, width_unz, depth_unz = frame.shape
    frame=cv2.resize(frame,(0,0), fx=(width_or/width_unz),fy=(height_or/height_unz))
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
	

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
