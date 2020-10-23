import pyglet
from pyglet.gl import *
import numpy as np
from math import sqrt, cos, sin, e, pi, floor
from random import random, randint
import scipy
from scipy.integrate import quad


class Vector():
    def __init__(self, speedm=1, scale=100, c=complex(1, 0)):
        self.speedm = speedm
        self.scale = scale

        # This costants can be expressed by c
        # self.init_angle = init_angle
        # self.r = r
        self.c = c

        self.t = None
        self.offset = None
        self.p = None
        self.x = None
        self.y = None

    def update(self, t, offset=complex(0, 0)):
        self.offset = offset

        # Using euler's formula, much cleaner
        self.p = self.c * \
            e**complex(0, 2*pi*t*self.speedm) + self.offset

        # self.p = (complex(self.r, 0)) * complex(cos((angle + self.init_angle) *
        #                                             self.speedm), sin((angle + self.init_angle)*self.speedm)) + self.offset
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


WSIZE = WIDHT, HEIGHT = (800, 800)
window = pyglet.window.Window(WIDHT, HEIGHT)

t = 0

drawing = []
maxx, maxy = 0, 0
with open("points10.txt") as f:
    for line in f.readlines():
        if line != "":
            x, y = line.rstrip("\n").split(",")
            maxx, maxy = max(maxx, float(x)), max(maxy, float(y))
            drawing.append([float(x), float(y)])

for i, d in enumerate(drawing):
    drawing[i] = [d[0] / maxx, d[1] / maxy]


def drawFromTXT(t):
    # T Ranges from 0 to 1
    l = len(drawing)
    index = floor(t*l)
    return complex(drawing[index][0], drawing[index][1])


vectors = []
for n in range(-2, 3):
    speed = n

    re, err = quad(lambda t: ((e**complex(-2*pi*n*t))
                              * drawFromTXT(t)).real, 0, 1)
    img, err = quad(lambda t: ((e**complex(-2*pi*n*t))
                               * drawFromTXT(t)).imag, 0, 1)

    # r = complex_quadrature(
    #     lambda t: (e**complex(-2*pi*n*t))*drawFromTXT(t), 0, 1)
    vectors.append(Vector(speedm=speed, scale=1, c=complex(re, img)))
    print(complex(re, img))

points = np.array([[0, 0]])


# vectors = [
#     Vector(speedm=i, scale=150, c=complex(1/i, 0)*e**complex(0, random()*2*pi)) for i in range(1, 50)
# ]
# C(n) = Intgr 0 -> 1 (f(t)e**(-n*2pi*i*t))


def on_draw(dt):
    window.clear()
    global t, points

    t += 0.1 * dt

    for i, vector in enumerate(vectors):
        if i == 0:
            vector.update(t)
        else:
            vector.update(t, vectors[i-1].p)

        vector.draw()

    # points = np.vstack([points, [[vectors[-1].x, vectors[-1].y]]])
    # pyglet.graphics.draw(len(points)-1, pyglet.gl.GL_LINE_STRIP,
    #                      ('v2f', (shift_coord(points[1:])).flatten()))


def shift_coord(points, offset=[WIDHT/2, HEIGHT/2]):
    return points + np.array(offset)


pyglet.clock.schedule_interval(on_draw, 1/144)

pyglet.app.run()
