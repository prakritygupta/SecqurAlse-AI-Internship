# -*- coding: utf-8 -*-
"""SecqurAIse Assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16tap1WFGnw0bkW6CPgIebTmuZghFvZSK
"""

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

def calculate_timestamp(start_time, current_frame, fps):
    return start_time + (current_frame / fps)

video_path = 'AI Assignment video.mp4'
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

quadrants = {
    1: [(0, frame_width // 2), 0, frame_height // 2],
    2: [(frame_width // 2, frame_width), 0, frame_height // 2],
    3: [(0, frame_width // 2), frame_height // 2, frame_height],
    4: [(frame_width // 2, frame_width), frame_height // 2, frame_height]
}

color_ranges = {
    'green': [(0, 0, 170), (50, 50, 255)],
   'orange': [(50, 100, 0), (90, 255, 255)],
    'white': [(20, 100, 100), (60, 255, 255)],
    'yellow': [(160, 100, 100), (200, 255, 255)]
}

output_txt_path = 'output.txt'

start_time = 0
current_quadrants = {color: {'quadrant': [0] * 4} for color in color_ranges.keys()}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    for color, color_range in color_ranges.items():
        mask = cv2.inRange(frame, np.array(color_range[0], dtype='uint8'), np.array(color_range[1], dtype='uint8'))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                x, y, w, h = cv2.boundingRect(contour)
                centroid = (x + w // 2, y + h // 2)

                for quadrant, (x_range, y_start, y_end) in quadrants.items():
                    if x_range[0] <= centroid[0] <= x_range[1] and y_start <= centroid[1] <= y_end:
                        ball_number = current_quadrants[color]['quadrant'].count(quadrant) + 1

                        if ball_number <= 4:
                            if current_quadrants[color]['quadrant'][ball_number - 1] != quadrant:
                                timestamp = calculate_timestamp(start_time, cap.get(cv2.CAP_PROP_POS_FRAMES), fps)
                                event_type = "Entry" if current_quadrants[color]['quadrant'][ball_number - 1] == 0 else "Exit"
                                entry_exit_record = f"Timestamp: {timestamp:.2f}s, Quadrant Number: {quadrant}, " \
                                                    f"Ball Colour: {color}, Ball Number: {ball_number}, Type: {event_type}"

                                with open(output_txt_path, 'a') as txt_file:
                                    txt_file.write(entry_exit_record + '\n')

                                current_quadrants[color]['quadrant'][ball_number - 1] = quadrant

                                cv2.putText(frame, f"{event_type} Q{quadrant} {color} Ball{ball_number}", (centroid[0] - 50, centroid[1]),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2_imshow(frame)

cap.release()
cv2.destroyAllWindows()