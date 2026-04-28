import cv2
import numpy as np
import mediapipe as mp
import math

# Initialize mediapipe hand detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Create canvas and colors
canvas = np.zeros((720, 1280, 3), np.uint8)
canvas.fill(255)  # Set the canvas background to white

# Initialize some variables
draw = False
color = (0, 0, 255)  # Default red
brush_size = 5
last_position = None
selected_color = (255, 255, 255)
paint_mode = False
stop_mode = False
eraser_mode = False
eraser_button_pressed = False
shape_mode = None
start_point = None

# Button positions and sizes
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]  # Blue, Green, Red, Yellow
brush_sizes = [5, 10, 15]
button_positions = {
    "colors": [(50, 50), (150, 50), (250, 50), (350, 50)],
    "brushes": [(1150, 50), (1150, 150), (1150, 250)],
    "clear": (50, 150),
    "paint": (50, 300),
    "eraser": (50, 375),
    "stop": (50, 450),
    "shapes": [(450, 50), (550, 50), (650, 50), (750, 50), (850, 50)]
}

# Undo/Redo functionality
history = []
redo_stack = []


# Function to draw based on history
def draw_history(canvas):
    canvas.fill(255)
    for action in history:
        if action[0] == 'line':
            cv2.line(canvas, action[1], action[2], action[3], action[4])
        elif action[0] == 'shape':
            draw_shape(canvas, action[1], action[2], action[3], action[4])


# Function to calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Function to draw buttons on the screen
def draw_buttons(frame):
    for i, pos in enumerate(button_positions['colors']):
        cv2.circle(frame, pos, 20, colors[i], -1)
        if color == colors[i] and not eraser_mode:  # Highlight selected color
            cv2.circle(frame, pos, 25, (0, 0, 0), 3)

    for i, pos in enumerate(button_positions['brushes']):
        cv2.circle(frame, pos, brush_sizes[i], (0, 0, 0), 2)
        if brush_size == brush_sizes[i]:  # Highlight selected brush size
            cv2.circle(frame, pos, brush_sizes[i] + 5, (0, 0, 0), 2)

    shapes = ["Square", "Rectangle", "Rhombus", "Arrow", "Triangle"]
    for i, pos in enumerate(button_positions['shapes']):
        if shapes[i] == "Square":
            cv2.rectangle(frame, (pos[0] - 15, pos[1] - 15), (pos[0] + 15, pos[1] + 15), (0, 0, 0), 2)
        elif shapes[i] == "Rectangle":
            cv2.rectangle(frame, (pos[0] - 20, pos[1] - 10), (pos[0] + 20, pos[1] + 10), (0, 0, 0), 2)
        elif shapes[i] == "Rhombus":
            pts = np.array(
                [[(pos[0], pos[1] - 15), (pos[0] + 15, pos[1]), (pos[0], pos[1] + 15), (pos[0] - 15, pos[1])]],
                np.int32)
            cv2.polylines(frame, pts, isClosed=True, color=(0, 0, 0), thickness=2)
        elif shapes[i] == "Arrow":
            cv2.arrowedLine(frame, (pos[0] - 10, pos[1]), (pos[0] + 10, pos[1] - 10), (0, 0, 0), 2)
        elif shapes[i] == "Triangle":
            pts = np.array([[(pos[0] - 15, pos[1] + 15), (pos[0] + 15, pos[1] + 15), (pos[0], pos[1] - 15)]], np.int32)
            cv2.polylines(frame, pts, isClosed=True, color=(0, 0, 0), thickness=2)

        if shape_mode == shapes[i].lower():
            cv2.rectangle(frame, (pos[0] - 25, pos[1] - 25), (pos[0] + 25, pos[1] + 25), (0, 255, 0), 2)

    # Clear button
    cv2.rectangle(frame, (button_positions['clear'][0] - 50, button_positions['clear'][1] - 30),
                  (button_positions['clear'][0] + 50, button_positions['clear'][1] + 30), (0, 0, 0), -1)
    cv2.putText(frame, "Clear", (button_positions['clear'][0] - 40, button_positions['clear'][1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Paint button
    cv2.rectangle(frame, (button_positions['paint'][0] - 50, button_positions['paint'][1] - 30),
                  (button_positions['paint'][0] + 50, button_positions['paint'][1] + 30),
                  (0, 255, 0) if paint_mode else (0, 0, 0), -1)
    cv2.putText(frame, "Paint", (button_positions['paint'][0] - 40, button_positions['paint'][1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Eraser button
    eraser_color = (255, 255, 255) if eraser_mode else (0, 0, 0)
    cv2.rectangle(frame, (button_positions['eraser'][0] - 50, button_positions['eraser'][1] - 30),
                  (button_positions['eraser'][0] + 50, button_positions['eraser'][1] + 30), eraser_color, -1)
    cv2.putText(frame, "Eraser", (button_positions['eraser'][0] - 40, button_positions['eraser'][1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0) if eraser_mode else (255, 255, 255), 2)

    # Stop button
    cv2.rectangle(frame, (button_positions['stop'][0] - 50, button_positions['stop'][1] - 30),
                  (button_positions['stop'][0] + 50, button_positions['stop'][1] + 30),
                  (0, 0, 255) if stop_mode else (0, 0, 0), -1)
    cv2.putText(frame, "Stop", (button_positions['stop'][0] - 40, button_positions['stop'][1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)


# Function to draw a selected shape
def draw_shape(canvas, start, shape, color, brush_size):
    if shape == "square":
        side_length = 100
        top_left = (min(start[0], start[0] + side_length), min(start[1], start[1] + side_length))
        cv2.rectangle(canvas, top_left, (top_left[0] + side_length, top_left[1] + side_length), color, brush_size)
    elif shape == "rectangle":
        width, height = 120, 80
        cv2.rectangle(canvas, start, (start[0] + width, start[1] + height), color, brush_size)
    elif shape == "rhombus":
        pts = np.array(
            [start, (start[0] + 60, start[1]), (start[0] + 30, start[1] + 60), (start[0] - 30, start[1] + 60)]).reshape(
            (-1, 1, 2))
        cv2.polylines(canvas, [pts], isClosed=True, color=color, thickness=brush_size)
    elif shape == "arrow":
        cv2.arrowedLine(canvas, start, (start[0] + 80, start[1] + 60), color, brush_size)
    elif shape == "triangle":
        pts = np.array([start, (start[0] + 60, start[1]), (start[0] + 30, start[1] + 60)]).reshape((-1, 1, 2))
        cv2.polylines(canvas, [pts], isClosed=True, color=color, thickness=brush_size)


# Smooth drawing using intermediate points
def smooth_line(prev, current, color, thickness):
    smooth_points = [prev, current]
    if prev and current:
        dist = calculate_distance(prev[0], prev[1], current[0], current[1])
        num_intermediate_points = int(dist / 5)  # Increase the number of points for smoother drawing
        for i in range(1, num_intermediate_points):
            interp_point = (int(prev[0] + (current[0] - prev[0]) * i / num_intermediate_points),
                            int(prev[1] + (current[1] - prev[1]) * i / num_intermediate_points))
            smooth_points.append(interp_point)
        for point in smooth_points:
            cv2.circle(canvas, point, thickness, color, -1)


# Handle button clicks (trigger action as soon as the finger enters the button area)
def handle_button_clicks(x, y):
    global color, brush_size, paint_mode, eraser_mode, shape_mode, start_point, last_position, stop_mode, eraser_button_pressed

    # Color buttons
    for i, pos in enumerate(button_positions['colors']):
        if calculate_distance(x, y, pos[0], pos[1]) < 20:
            color = colors[i]
            eraser_mode = False  # Deselect eraser when a color is selected

    # Brush size buttons
    for i, pos in enumerate(button_positions['brushes']):
        if calculate_distance(x, y, pos[0], pos[1]) < brush_sizes[i]:
            brush_size = brush_sizes[i]

    # Clear button
    if calculate_distance(x, y, button_positions['clear'][0], button_positions['clear'][1]) < 50:
        canvas.fill(255)  # Clear the canvas
        history.clear()
        redo_stack.clear()

    # Paint button
    if calculate_distance(x, y, button_positions['paint'][0], button_positions['paint'][1]) < 50:
        paint_mode = True
        stop_mode = False
        eraser_mode = False  # Deselect eraser when paint mode is active

    # Eraser button
    eraser_button_center = button_positions['eraser']
    if calculate_distance(x, y, eraser_button_center[0], eraser_button_center[1]) < 50:
        eraser_mode = not eraser_mode
        eraser_button_pressed = True  # Mark that the button was interacted with
    elif eraser_button_pressed:
        # If the finger leaves the button area, keep the state
        pass

    # Stop button
    if calculate_distance(x, y, button_positions['stop'][0], button_positions['stop'][1]) < 50:
        stop_mode = True
        paint_mode = False
        eraser_mode = False  # Deselect eraser when stop mode is active

    # Shape buttons
    shapes = ["square", "rectangle", "rhombus", "arrow", "triangle"]
    for i, pos in enumerate(button_positions['shapes']):
        if calculate_distance(x, y, pos[0], pos[1]) < 25:
            shape_mode = shapes[i]
            eraser_mode = False  # Deselect eraser when a shape is selected


# Main function to run air canvas
def run_air_canvas():
    global draw, last_position, history, redo_stack, start_point, shape_mode, paint_mode, stop_mode, eraser_mode, eraser_button_pressed

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Set width
    cap.set(4, 720)  # Set height

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        small_frame = cv2.resize(frame, (640, 360))

        small_frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        results = hands.process(small_frame_rgb)
        hand_landmarks = results.multi_hand_landmarks

        if hand_landmarks:
            for landmarks in hand_landmarks:
                x, y = int(landmarks.landmark[8].x * 1280), int(landmarks.landmark[8].y * 720)
                middle_x, middle_y = int(landmarks.landmark[12].x * 1280), int(landmarks.landmark[12].y * 720)

                distance = calculate_distance(x, y, middle_x, middle_y)

                if distance < 50 and paint_mode and not stop_mode:  # Gesture made and paint mode active
                    if shape_mode:  # If a shape is selected
                        if start_point is None:
                            start_point = (x, y)
                        else:
                            draw_shape(canvas, start_point, shape_mode, color if not eraser_mode else (255, 255, 255),
                                       brush_size)
                            history.append(('shape', start_point, shape_mode, color, brush_size))
                            redo_stack.clear()
                            start_point = None
                            shape_mode = None
                    else:
                        if last_position is None:
                            last_position = (x, y)
                        else:
                            smooth_line(last_position, (x, y), color if not eraser_mode else (255, 255, 255),
                                        brush_size)
                            last_position = (x, y)
                            history.append(('line', last_position, (x, y), color, brush_size))
                            redo_stack.clear()
                else:
                    last_position = None
                    start_point = None
                    eraser_button_pressed = False  # Reset the button press state when not drawing

                handle_button_clicks(x, y)
                mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        draw_buttons(frame)

        cv2.addWeighted(canvas, 0.7, frame, 0.3, 0, frame)

        cv2.imshow("Air Canvas", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('u') and history:
            redo_stack.append(history.pop())
            draw_history(canvas)
        elif key == ord('r') and redo_stack:
            history.append(redo_stack.pop())
            draw_history(canvas)

    cap.release()
    cv2.destroyAllWindows()

# Run the air canvas
run_air_canvas()

