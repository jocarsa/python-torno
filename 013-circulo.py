import cv2
import numpy as np
import random
import time
import os
import math

# Video properties
width, height = 1920, 1080
fps = 60
duration = 60  # seconds
total_frames = fps * duration
rotation_per_frame = 360 / (fps * 5)  # 1 turn per 5 seconds

# Create a blank white canvas
canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

# Prepare the folder and filename
epoch_time = int(time.time())
render_folder = 'render'
os.makedirs(render_folder, exist_ok=True)
output_filename = os.path.join(render_folder, f'{epoch_time}_lathe_drawing.mp4')

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

# Initialize brush position and properties
x, y = width/2, height/2
brush_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
direction = math.pi * 2

# Center of the image and radius of the imaginary circle
center_x, center_y = width // 2, height // 2
radius = height // 2

# Start time
start_time = time.time()

for frame_num in range(total_frames):
    
    # Rotate the canvas
    rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), rotation_per_frame * frame_num, 1)
    rotated_canvas = cv2.warpAffine(canvas, rotation_matrix, (width, height), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
    
    # Update brush direction with some random fluctuation
    direction += random.uniform(-0.1, 0.1)
    
    # Move the brush
    x += math.cos(direction)
    y += math.sin(direction)
    
    # Calculate the distance from the center of the circle
    distance_from_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    
    # If the brush is outside the circle, reflect the direction
    if distance_from_center > radius:
        # Calculate angle of the brush relative to the center
        angle_to_center = math.atan2(center_y - y, center_x - x)
        
        # Reflect the direction across the angle to the center
        direction = 2 * angle_to_center - direction + math.pi
        
        # Move the brush back within the boundary of the circle
        x = center_x + radius * math.cos(direction)
        y = center_y + radius * math.sin(direction)

    # Convert x and y to integers
    x_int, y_int = int(x), int(y)
    
    # Gradually change the brush color
    brush_color[0] = (brush_color[0] + random.randint(-1, 1)) % 256
    brush_color[1] = (brush_color[1] + random.randint(-1, 1)) % 256
    brush_color[2] = (brush_color[2] + random.randint(-1, 1)) % 256
    
    # Draw the brush (marker) on the rotated canvas
    cv2.circle(rotated_canvas, (x_int, y_int), 10, tuple(brush_color), -1)
    
    # Update the canvas with the new drawing (rotate it back to the original orientation)
    canvas = cv2.warpAffine(rotated_canvas, rotation_matrix, (width, height), flags=cv2.WARP_INVERSE_MAP, borderValue=(255, 255, 255))
    
    # Print statistics every 60 frames
    if frame_num % 60 == 0:
        elapsed_time = time.time() - start_time
        time_remaining = (total_frames - frame_num) / fps
        estimated_finish = start_time + (elapsed_time / (frame_num + 1)) * total_frames
        percentage_complete = (frame_num + 1) / total_frames * 100

        # Print statistics to the console
        print(f'Frame: {frame_num}/{total_frames} | Time Passed: {elapsed_time:.2f}s | '
              f'Time Remaining: {time_remaining:.2f}s | '
              f'Estimated Finish: {time.strftime("%H:%M:%S", time.localtime(estimated_finish))} | '
              f'Completion: {percentage_complete:.2f}%')
    
    # Write the frame to the video
    video_writer.write(rotated_canvas)

# Release the video writer
video_writer.release()
cv2.destroyAllWindows()

print(f'Video has been saved to {output_filename}')
