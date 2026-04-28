# Air-Craft-Your-Virtual-Canvas
Draw in the air using just your hand gestures.
This project uses OpenCV and MediaPipe to track hand movements via webcam and convert them into a real-time virtual drawing experience.

---

## Features
* Air Drawing : Draw freely using hand gestures on a virtual canvas
* Color Selection : Choose from multiple colors (Blue, Green, Red, Yellow)
* Brush Sizes : Adjust thickness of drawing strokes
* Eraser Mode : Remove drawings easily
* Paint / Stop Modes : Enable or disable drawing
* Shape Drawing :
  * Square
  * Rectangle
  * Rhombus
  * Arrow
  * Triangle
* Clear Canvas : Reset the entire drawing area
* Smooth Drawing : Interpolated points for fluid lines
* Live Hand Tracking : Real-time detection using MediaPipe

---

## Requirements
Make sure you have Python 3.7+ installed. Then install dependencies:

```bash
pip install opencv-python mediapipe numpy
```

---

##Usage
1. Clone this repository:

```bash
git clone https://github.com/TheUnpigmentedRex/AirCraft-Virtual-Canvas.git
cd AirCraft-Virtual-Canvas
```

2. Run the script:

```bash
python main.py
```

3. A webcam window will open. Use your hand to draw and interact with buttons

4. Press q to exit

---

## Gesture Mappings
* Bring index & middle finger close : Draw
* Hover over buttons : Select tools
* Move index finger : Draw / Navigate
* Press q : Quit

---

