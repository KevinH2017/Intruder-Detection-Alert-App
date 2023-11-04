import cv2, time, glob, os, threading
from image_send_email import send_email

# 0 is default camera, 1 is external / secondary camera
video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

def clean_folder():
    """Permanently deletes all .png files in images folder"""
    print("clean_folder function started!")
    images = glob.glob("./app9/images/*.png")
    for image in images:
        os.remove(image)
    print("clean_folder function ended!")
    
while True:
    status = 0
    # Gets video data and converts it to gray
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    # Calculations to determine if an object is in frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Creates rectangle around detected object
    contours, check = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 3)
        # If object detection is True, sets status = 1
        # If True, saves images in "images" folder
        if rectangle.any():
            status = 1
            cv2.imwrite(f"./app9/images/{count}.png", frame)
            count += 1      
            all_images = glob.glob("./app9/images/*.png")
            index = int(len(all_images) / 2)
            image_detect = all_images[index]
    
    status_list.append(status)
    status_list = status_list[-2:]

    # Only when status_list has both 0 and 1 does email_thread and clean_folder_thread run
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = threading.Thread(target=send_email, args=(image_detect, ))
        email_thread.daemon = True

        clean_folder_thread = threading.Thread(target=clean_folder)
        clean_folder_thread.daemon = True

        email_thread.start()
        
    cv2.imshow("My Video", frame)
    key = cv2.waitKey(1)

    # Breaks loop when "q" is pressed
    if key == ord("q"):
        break

video.release()
# Below runs only when user quits program
clean_folder_thread.start()