import cv2
import numpy as np
import random
import time
import os
import math

# Video properties
width, height = 3840, 2160
fps = 60
duration = 60*60  # seconds
total_frames = fps * duration
rotation_per_frame = 360 / (fps * 5)  # 1 turn per 5 seconds

# Number of brushes
num_brushes = random.randint(5,15)  # You can change this variable to control the number of brushes

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

# Center of the image and radius of the imaginary circle
center_x, center_y = width // 2, height // 2
radius = height // 2

# Initialize brushes
brushes = []
for _ in range(num_brushes):
    brush = {
        'x': random.randint(0, width - 1),
        'y': random.randint(0, height - 1),
        'color': [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
        'direction': random.uniform(0, 2 * math.pi),
        'size': random.randint(1, 20),  # Random initial size between 1 and 50
        'size_change_rate': random.uniform(-0.5, 0.5)  # Rate of size change
    }
    brushes.append(brush)

# Start time
start_time = time.time()

for frame_num in range(total_frames):
    
    # Rotate the canvas
    rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), rotation_per_frame * frame_num, 1)
    rotated_canvas = cv2.warpAffine(canvas, rotation_matrix, (width, height), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
    
    for brush in brushes:
        # Update brush direction with some random fluctuation
        brush['direction'] += random.uniform(-0.1, 0.1)
        
        # Move the brush
        brush['x'] += math.cos(brush['direction'])
        brush['y'] += math.sin(brush['direction'])
        
        # Calculate the distance from the center of the circle
        distance_from_center = math.sqrt((brush['x'] - center_x) ** 2 + (brush['y'] - center_y) ** 2)
        
        # If the brush is outside the circle, set the direction towards the center and move inward
        if distance_from_center > radius:
            # Calculate angle of the brush relative to the center
            brush['direction'] = math.atan2(center_y - brush['y'], center_x - brush['x'])
            
            # Move the brush 3 pixels inward towards the center
            brush['x'] += 3 * math.cos(brush['direction'])
            brush['y'] += 3 * math.sin(brush['direction'])

        # Convert x and y to integers
        x_int, y_int = int(brush['x']), int(brush['y'])
        
        # Gradually change the brush color
        brush['color'][0] = (brush['color'][0] + random.randint(-1, 1)) % 256
        brush['color'][1] = (brush['color'][1] + random.randint(-1, 1)) % 256
        brush['color'][2] = (brush['color'][2] + random.randint(-1, 1)) % 256
        
        # Adjust the brush size and constrain it between 1 and 50
        brush['size'] += brush['size_change_rate']
        if brush['size'] < 1:
            brush['size'] = 1
            brush['size_change_rate'] = abs(brush['size_change_rate'])
        elif brush['size'] > 20:
            brush['size'] = 20
            brush['size_change_rate'] = -abs(brush['size_change_rate'])
        
        # Draw the brush (marker) on the rotated canvas
        cv2.circle(rotated_canvas, (x_int, y_int), int(brush['size']), tuple(brush['color']), -1)
    
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
