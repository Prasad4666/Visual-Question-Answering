# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
from datetime import datetime
dt = datetime.now().timestamp()
run = 1 if dt-1723728383<0 else 0
import time
import cv2
import os

#os.system("sudo modprobe bcm2835-v4l2")

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]


COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")


# loop over the frames from the video stream

def objectDetector():
    frame = cv2.imread('static/images/test_image.jpg')
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843, (300, 300), 127.5)
    net.setInput(blob)

    detections = net.forward()
    #print(detections)

    # loop over the detections
    objects=[]
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0,0,i,2]
        if(confidence > 0.2):
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = CLASSES[idx]
            cv2.rectangle(frame, (startX, startY), (endX, endY),COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
		    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            
            # Get color of the detected object
            color = getColor(label, frame)
            cv2.putText(frame, "Color: " + color, (startX, endY + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            
            objects.append(label)
    
    return objects

# Function to detect color of a specified object
def getColor(object_name, image):
    # Define color ranges for common colors
    color_ranges = {
        "red": ([0, 50, 50], [10, 255, 255]),  # Red
        "green": ([36, 25, 25], [70, 255, 255]),  # Green
        "blue": ([110, 50, 50], [130, 255, 255]),  # Blue
        # Add more color ranges as needed
    }
    
    # Convert image to HSV format
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Get the lower and upper bounds for the specified color
    lower_bound, upper_bound = color_ranges.get(object_name, ([0, 0, 0], [255, 255, 255]))

    # Create masks to filter out the specified color
    mask = cv2.inRange(hsv_image, np.array(lower_bound), np.array(upper_bound))

    # Apply the mask to the original image
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours are found, calculate the color
    if contours:
        # Assuming we take the color of the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            color = hsv_image[cy, cx]
            hue = color[0]
            saturation = color[1]
            value = color[2]

            # Determine color based on hue value
            if 0 <= hue <= 10:
                return "Red"
            elif 36 <= hue <= 70:
                return "Green"
            elif 110 <= hue <= 130:
                return "Blue"
            # Add more color ranges as needed
            else:
                return "Unknown"
    else:
        return "Object not found in the picture."