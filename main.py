import pyglet
from pyglet.gl import *
import numpy as np
from math import sqrt, cos, sin
from random import random, randint


class Vector():
    def __init__(self, r=1, speedm=1, init_angle=0, scale=100):
        self.r = r
        self.speedm = speedm
        self.scale = scale
        self.init_angle = init_angle

        self.angle = None
        self.offset = None
        self.p = None
        self.x = None
        self.y = None

    def update(self, angle, offset=complex(0, 0)):
        self.offset = offset
        self.p = (complex(self.r, 0)) * complex(cos((angle + self.init_angle) *
                                                    self.speedm), sin((angle + self.init_angle)*self.speedm)) + self.offset
        self.x, self.y = self.p.real*self.scale, self.p.imag*self.scale

    def draw(self):
        glBegin(GL_LINES)
        glVertex2f(
            self.offset.real*self.scale + WIDHT/2,
            self.offset.imag*self.scale + HEIGHT/2
        )
        glVertex2f(
            self.x + WIDHT/2,
            self.y + HEIGHT/2
        )
        glEnd()

        # pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES,
        #                      ('v2f', (self.x + WIDHT/2,
        #                               self.y + HEIGHT/2, self.x + WIDHT/2 + 5,
        #                               self.y + HEIGHT/2+5, self.x + WIDHT/2-5,
        #                               self.y + HEIGHT/2-5))
        #                      )

        # pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES,
        #                      ('v2f', (self.x + WIDHT/2,
        #                               self.y + HEIGHT/2,
        #                               0, 0,
        #                               0, 50))
        #                      )


WSIZE = WIDHT, HEIGHT = (1000, 1000)
window = pyglet.window.Window(WIDHT, HEIGHT)

a = 0

vectors = [
    Vector(r=1/i, speedm=i, init_angle=random()*6.28, scale=200) for i in range(1, 50)
]

points = np.array([[0, 0]])

# v1 = Vector(r=1, speedm=1, scale=100)
# v2 = Vector(r=0.5, speedm=2, scale=100)

# vectors = [v1, v2]


def on_draw(dt):
    window.clear()
    global a, points

    a += 0.5 * dt

    for i, vector in enumerate(vectors):
        if i == 0:
            vector.update(a)
        else:
            vector.update(a, vectors[i-1].p)

        vector.draw()

    points = np.vstack([points, [[vectors[-1].x, vectors[-1].y]]])
    pyglet.graphics.draw(len(points)-1, pyglet.gl.GL_LINE_STRIP,
                         ('v2f', (shift_coord(points[1:])).flatten()))

    points = np.unique(points, axis=1)


def shift_coord(points, offset=[WIDHT/2, HEIGHT/2]):
    return points + np.array(offset)


pyglet.clock.schedule_interval(on_draw, 1/144)

pyglet.app.run()
