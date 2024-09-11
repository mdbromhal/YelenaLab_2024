#!/usr/bin/env python3

# Author: Megdalia Bromhal & COPILOT AI
# Date: 11 Sept. 2024
# Purpose: Testing tflite and coco packages just installed

# ***RUN IN tensorflowenv VIRTUAL ENVIRONMENT FOR TENSORFLOW LITE PACKAGE***

import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

try:
    # Load TFLite model & allocate tensors
    interpreter = tflite.Interpreter(model_path="CoCo_TFlite/detect.tflite")
    interpreter.allocate_tensors() # /home/mickey/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load an image
    image = cv2.imread('/home/mickey/scripts/Yelena_dfs/photos/2024-09-11-16-20-24.jpg')
    input_data = cv2.resize(image, (300, 300))
    input_data = np.expand_dims(input_data, axis=0)

    # Run the model
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Get results
    output_data = interpreter.get_tensor(output_details[0]['index'])
    class_ids = interpreter.get_tensor(output_details[1]['index'])
    scores = interpreter.get_tensor(output_details[2]['index'])
    print(output_data)
    
    for i in range(len(scores[0])):
        if scores[0][i] > 0.5: # Confidence threshold
            print(f"Class ID: {class_ids[0][i]}, Score: {scores[0][1]}, Box: {output_data[0][i]}")

except Exception as e:
    print(f"Error loading model: {e}")
