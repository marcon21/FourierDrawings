import pyglet 
import numpy as np
from math import sqrt, cos, sin

WSIZE = WIDHT, HEIGHT = (800, 800)
window = pyglet.window.Window(WIDHT, HEIGHT)

@window.event
def on_draw():
    window.clear()

    points = np.array([[0,0]])

    # step_size = 0.05

    # for x in range(int(-100*(1/step_size)), int(100*(1/step_size))):
    #     points = np.vstack([points, [[x*step_size, sqrt(r*r - (x*step_size)**2)]]])
    #     points = np.vstack([points, [[x*step_size, -sqrt(r*r - (x*step_size)**2)]]])

    # for x in range(int(-100*(1/step_size)), int(100*(1/step_size))):
    #     y1, y2 = circle(x*step_size)
    #     points = np.vstack([points, [[x*step_size, y1]]])
    #     points = np.vstack([points, [[x*step_size, y2]]])

    steps = 1000
    for i in np.linspace(0, 360, steps):
        p = complex(1, 0) * complex(cos(i), sin(i))
        points = np.vstack([points, [[p.real*100, p.imag*100]]])

    print(points)
    pyglet.graphics.draw(len(points), pyglet.gl.GL_POINTS,
        ('v2f', (shift_coord(points)).flatten()))

def shift_coord(points, offset=[WIDHT/2, HEIGHT/2]):
    return points + np.array(offset)

# def circle(x, r=100):
#     return sqrt(r**2 - x**2), -sqrt(r**2 - x**2) 


pyglet.clock.schedule_interval(foo, 1.0)

pyglet.app.run()
