import cv2
import numpy as np
import random
import time
import os

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

# Initialize brush position (in world coordinates)
x, y = width // 2, height // 2
brush_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Start time
start_time = time.time()

for frame_num in range(total_frames):
    # Move the marker randomly (simulating hand movement)
    dx = random.randint(-10, 10)
    dy = random.randint(-10, 10)
    x = np.clip(x + dx, 0, width - 1)
    y = np.clip(y + dy, 0, height - 1)
    
    # Draw the marker on the rotating canvas
    cv2.circle(canvas, (x, y), 10, brush_color, -1)
    
    # Rotate the entire canvas
    rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), rotation_per_frame * frame_num, 1)
    rotated_canvas = cv2.warpAffine(canvas, rotation_matrix, (width, height), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
    
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
