#!/usr/bin/env python3

# Author: Megdalia Bromhal & COPILOT AI
# Date: 11 Sept. 2024
# Purpose: Testing tflite and coco packages just installed

# ***RUN IN tensorflowenv VIRTUAL ENVIRONMENT FOR TENSORFLOW LITE PACKAGE***
# You don't actually have to...

import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import time

# Loading CoCo class labels - From ChatGPT
def load_labels():
    labels = []
    with open("CoCo_TFlite/labelmap.txt", 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    return labels

# Below is mostly from https://blog.paperspace.com/tensorflow-lite-raspberry-pi/
try:
    # Load TFLite model & allocate tensors
    interpreter = tflite.Interpreter(model_path="CoCo_TFlite/detect.tflite")
    interpreter.allocate_tensors() # /home/mickey/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load an image
    #image = cv2.imread('/home/mickey/scripts/Yelena_dfs/photos/2024-09-11-16-20-24.jpg')
    
    # Capture an image
    cap = cv2.VideoCapture(0)
    
    ret, test_image = cap.read()
    frame_height, frame_width, _ = test_image.shape
    
    timestamp = time.strftime('%d.%m.%Y-%H.%M.%S')
    
    # Defining how to record video - https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'obj_detect_photos/detection_test_{timestamp}.mp4', fourcc, 20.0, (frame_width, frame_height))
    
    # Running while True will make it more like live video feed
    while True:
        ret, image = cap.read()
        
        height, width, _ = image.shape # From ChatGPT
        input_data = cv2.resize(image, (300, 300))
        input_data = np.expand_dims(input_data, axis=0)

        # Run the model
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Get results
        output_data = interpreter.get_tensor(output_details[0]['index'])
        class_ids = interpreter.get_tensor(output_details[1]['index'])
        scores = interpreter.get_tensor(output_details[2]['index'])
        #print(output_data)
        
        # Load labels - from ChatGPT
        labels = load_labels()
        
        for i in range(len(scores[0])):
            if scores[0][i] > 0.5: # Confidence threshold
                #print(f"Class ID: {class_ids[0][i]}, Score: {scores[0][1]}, Box: {output_data[0][i]}")
                # From ChatGPT
                class_id = int(class_ids[0][i])
                score = scores[0][i]
                box = output_data[0][i]
                
                # Convert box coordinates to original image dimensions
                y_min = int(box[0] * height)
                x_min = int(box[1] * width)
                y_max = int(box[2] * height)
                x_max = int(box[3] * width)
                
                # Draw bounding box
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
                
                # Draw label
                label = f"{labels[class_id]}: {score:.2f}"
                cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                print(label)
        
        # Write the frame to the output file
        out.write(image)
    
        # Write image with detections
        #cv2.imwrite(f"obj_detect_photos/Detections_test_{timestamp}.jpg", image)
        
        # Show image with detections
        cv2.imshow('Detections', image)
        # cv2.waitKey(1)
        #cv2.destroyAllWindows()
        
        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break
        
    # Release the capture and writer objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()
            
except Exception as e:
    print(f"Error loading model: {e}")
# Eof