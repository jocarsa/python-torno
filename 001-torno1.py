import cv2
import numpy as np
import random

# Video properties
width, height = 1920, 1080
fps = 60
duration = 60  # seconds
total_frames = fps * duration
rotation_per_frame = 360 / (fps * 5)  # 1 turn per 5 seconds

# Create a blank white canvas
canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter('lathe_drawing.mp4', fourcc, fps, (width, height))

# Initialize brush position
x, y = width // 2, height // 2
brush_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

for frame_num in range(total_frames):
    # Random small movement for the brush
    dx = random.randint(-10, 10)
    dy = random.randint(-10, 10)
    x = np.clip(x + dx, 0, width - 1)
    y = np.clip(y + dy, 0, height - 1)
    
    # Draw on the canvas
    cv2.circle(canvas, (x, y), 2, brush_color, -1)
    
    # Rotate the canvas
    rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), rotation_per_frame * frame_num, 1)
    rotated_canvas = cv2.warpAffine(canvas, rotation_matrix, (width, height), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
    
    # Write the frame to the video
    video_writer.write(rotated_canvas)

# Release the video writer
video_writer.release()
cv2.destroyAllWindows()
