import cv2
import numpy as np

def draw_grid(frame):
    """
    Draws a 3×3 overlay grid on the frame.
    This grid visually matches the extraction logic in face_detector.py.
    """
    h, w, _ = frame.shape

    # Margin sizes (match face_detector.py)
    margin_w = int(w * 0.20)
    margin_h = int(h * 0.15)

    # Main grid area size
    grid_w = w - 2 * margin_w
    grid_h = h - 2 * margin_h

    cell_w = grid_w // 3
    cell_h = grid_h // 3

    # Top-left corner of grid
    x0 = margin_w
    y0 = margin_h

    # Colors for overlay
    line_color = (0, 255, 0)  # bright green
    thickness = 2

    # Draw outer rectangle
    cv2.rectangle(frame, (x0, y0), (x0 + grid_w, y0 + grid_h), line_color, thickness)

    # Draw vertical lines
    for i in range(1, 3):
        x = x0 + i * cell_w
        cv2.line(frame, (x, y0), (x, y0 + grid_h), line_color, thickness)

    # Draw horizontal lines
    for i in range(1, 3):
        y = y0 + i * cell_h
        cv2.line(frame, (x0, y), (x0 + grid_w, y), line_color, thickness)

    # Optional: Draw small dots in the centers of each cell for easier alignment
    for row in range(3):
        for col in range(3):
            cx = x0 + col * cell_w + cell_w // 2
            cy = y0 + row * cell_h + cell_h // 2
            cv2.circle(frame, (cx, cy), 4, (0, 255, 255), -1)

    return frame
