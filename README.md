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

## Demo Pictures
## Picture 1: Hand Tracking
![Pic 1](https://github.com/TheUnpigmentedRex/Air-Craft-Your-Virtual-Canvas/blob/main/Landmarks_on_the_palm.png)
This shows the live hand tracking with landmarks drawn on the webcam feed.

---

## Picture 2: Paint Mode
![Pic 2](https://github.com/TheUnpigmentedRex/Air-Craft-Your-Virtual-Canvas/blob/main/Paint_Demo.png)
Drawing on the canvas using finger gesture: BrInging the Index and Middle Fingers close to one another.

---

## Picture 3: Different Brush Strokes
![Pic 3](https://github.com/TheUnpigmentedRex/Air-Craft-Your-Virtual-Canvas/blob/main/Different_Brushes.png)
A variety of Brush Strokes are available as shown above.

---

## Picture 4: Different Colour Options
![Pic 4](https://github.com/TheUnpigmentedRex/Air-Craft-Your-Virtual-Canvas/blob/main/Different_Colours.png)
A variety of Colour Options are available as shown above.

---

## Picture 5: Different Shapes 
![Pic 5](https://github.com/TheUnpigmentedRex/Air-Craft-Your-Virtual-Canvas/blob/main/Different_Shapes.png)
A variety of Shapes are available as shown above.

---

## Picture 6: Erase Mode
![Pic 6](https://github.com/TheUnpigmentedRex/Air-Craft-Your-Virtual-Canvas/blob/main/Eraser_Demo.png)
Erasing parts of the drawing using gesture-based eraser.

---

## Picture 7: Stop Mode
![Pic 7](https://github.com/TheUnpigmentedRex/Air-Craft-Your-Virtual-Canvas/blob/main/Stop_Demo.png)
No Painting, when Stop is enabled, even if the drawing gesture is made.

---

## Picture 8: Writing Demo 
![Pic 8](https://github.com/TheUnpigmentedRex/Air-Craft-Your-Virtual-Canvas/blob/main/Writing_Demo.png)
The above shows a random written piece using the Air Craft.

---

## Demo Video
[![Watch Demo](https://img.youtube.com/vi/mlkWxCmua18/0.jpg)](https://www.youtube.com/watch?v=mlkWxCmua18)

---
