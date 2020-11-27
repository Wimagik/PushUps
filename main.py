import cv2
import time

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

high_pos = 40
low_pos = 275
y = 0
pos = "None"
nb_pushUps = 0
breaking = False
while not breaking:
    choice = int(input("1 pour initialiser la position haute,\n"
                       "2 pour basse,\n"
                       "3 pour lancer : "))

    if choice == 1 or choice == 2:
        countdown = 3
        print(countdown)
    init_time = time.monotonic()

    # To capture video from webcam.
    videocap = cv2.VideoCapture(0)
    # To use a video file as input -> videocap = cv2.VideoCapture('filename.mp4')

    while True:

        # Read the frame
        _, img = videocap.read()


        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the face
        faces = face_cascade.detectMultiScale(gray, 1.1, 6)

        # Draw the rectangle around the face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Display
        cv2.imshow('img', img)
        if choice == 1 or choice ==2:
            if init_time+1<time.monotonic():
                init_time = time.monotonic()
                if countdown > 0:
                    countdown = countdown-1
                    print(countdown)
                else:
                    if choice == 1:
                        high_pos=y
                        print("pos haute = ",y)
                        break
                    elif choice == 2:
                        low_pos=y
                        print("pos basse = ",y)
                        break
        if choice == 3:
            if init_time+0.3<=time.monotonic():
                if high_pos-25 <= y <= high_pos+25:
                    if pos != "haut":
                        pos = "haut"
                        #not RGB but BGR
                        cv2.rectangle(img, (0, high_pos+25), (800, high_pos-25), (0, 255, 0), 2)
                        cv2.rectangle(img, (0, low_pos+25), (800, low_pos-25), (0, 0, 255), 2)

                elif low_pos-25 <= y <= low_pos+25:
                    if pos != "bas":
                        if pos == "haut":  # si la pos précédente = haut
                            nb_pushUps += 1
                            print(nb_pushUps)
                            cv2.rectangle(img, (0, high_pos+25), (800, high_pos-25), (0, 0, 255), 2)
                            cv2.rectangle(img, (0, low_pos+25), (800, low_pos-25), (0, 255, 0), 2)
                        pos="bas"
                init_time=time.monotonic()

        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            breaking = True
            break

# Release the VideoCapture object
videocap.release()
