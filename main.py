import pyglet 
import numpy as np
from math import sqrt


WSIZE = WIDHT, HEIGHT = (800, 800)

window = pyglet.window.Window(WIDHT, HEIGHT)


@window.event
def on_draw():
    window.clear()

    points = np.array([[0,0]])

    step_size = 0.05
    r = 100
    for x in range(int(-100*(1/step_size)), int(100*(1/step_size))):
        points = np.vstack([points, [[x*step_size, sqrt(r*r - (x*step_size)**2)]]])
        points = np.vstack([points, [[x*step_size, -sqrt(r*r - (x*step_size)**2)]]])

    pyglet.graphics.draw(len(points), pyglet.gl.GL_POINTS,
        ('v2f', (shift_coord(points)).flatten()))

def shift_coord(points, offset=[WIDHT/2, HEIGHT/2]):
    return points + np.array(offset)

pyglet.app.run()
