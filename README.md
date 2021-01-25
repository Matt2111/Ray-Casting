# Ray-Casting

"Rays linesweep.py" demonstrates ray casting using the line-sweep algorithm. Rays are cast from the mouse point and can be seen by pressing the left mouse button. It also includes a vertex detection algorithm which massively boosts resolution without a big performance hit like increasing the base ray count, you can toggle this by clicking the spacebar.

Example 1, this has 45 rays with vertex detection on.
![Alt text](https://raw.githubusercontent.com/Matt2111/Ray-Casting/main/Images/45%20Rays%20Vertex%20Detection.png)

Example 2, this has 45 rays with vertex detection off.
![Alt text](https://github.com/Matt2111/Ray-Casting/blob/main/Images/45%20Rays.png)

Example 3, this has 45 rays with vertex detection off and visible rays. (red = missed ray, green = collided ray, blue = new vertex detection ray)
![Alt text](https://raw.githubusercontent.com/Matt2111/Ray-Casting/main/Images/45%20Rays%20Visible.png)

Example 4, this had 45 rays with vertex detection and visible rays. (red = missed ray, green = collided ray, blue = new vertex detection ray)
![Alt text](https://raw.githubusercontent.com/Matt2111/Ray-Casting/main/Images/45%20Rays%20Visible%20Vertex%20Detection.png)
