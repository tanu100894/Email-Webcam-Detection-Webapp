import cv2
import time, glob
from emailing import send_email


# Open the webcam (0 = default camera)
video = cv2.VideoCapture(0)     # 1 is used for using secondary camera.

# Wait for 1 second to allow the camera to warm up
time.sleep(1)

first_frame = None  # Will store the first captured frame (used as reference for motion detection)
status_list = []
count = 1

while True:
    status = 0
    # Read a frame from the webcam
    check, frame = video.read()

    # Convert the frame to grayscale (simplifies the image)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and improve motion detection
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (15, 15), 0)

    # Store the first frame as a baseline for comparison
    if first_frame is None:
        first_frame = gray_frame_gau
        continue  # Skip rest of the loop on first iteration

    # Compute the absolute difference between the current frame and the first frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Apply threshold to highlight differences (motion areas)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded image to fill in holes (connect broken regions)
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Display the binary image showing detected motion
    cv2.imshow("My Video", dil_frame)

    # Find contours from the dilated image
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw rectangles around significant contours (i.e., areas of movement)
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue  # Ignore small areas of change (like noise)

        # Get coordinates of the bounding box around the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Draw a green rectangle on the original frame
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email(image_with_object)

    # Show the original frame with bounding boxes
    cv2.imshow("Live Feed", frame)

    # Break the loop when 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Release the webcam and close all OpenCV windows
video.release()
cv2.destroyAllWindows()