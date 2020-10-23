import pyglet
from pyglet.gl import *
import numpy as np
from math import sqrt, cos, sin, e, pi, floor
from random import random, randint
import sys, getopt

class Vector():
    def __init__(self, frequency=1, scale=100, c=complex(1, 0)):
        self.frequency = frequency
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

        # Using euler's rappresentation, much cleaner and cooler tbh
        self.p = self.c * \
            e**complex(0, 2*pi*t*self.frequency) + self.offset

        # self.p = (complex(self.r, 0)) * complex(cos((angle + self.init_angle) *
        #                                             self.frequency), sin((angle + self.init_angle)*self.frequency)) + self.offset
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

# Maps the points of the drawing to a function
def drawFromTXT(t):
    # T Ranges from 0 to 1
    l = len(drawing)
    index = floor(t*l) - 1

    return complex(drawing[index][0], -drawing[index][1])

def importTXT(filename):
    drawing = np.array([[0, 0]])

    # A list of point in format x,y
    # I absolutely recommend the use of https://github.com/Shinao/PathToPoints 
    with open(filename) as f:
        for line in f.readlines():
            if line != "":
                x, y = line.rstrip("\n").split(",")
                drawing = np.vstack([drawing, [[float(x), float(y)]]])

    # Normalizing and shifting the list of points
    drawing = (drawing[1:] - drawing[1:].max(axis=0) / 2) / drawing[1:].max(axis=0)
    return drawing


# Finding all the parameters for each vector
# Probably the coolest part of the project
def init_vectors(nn, steps=1000, scale=0.5):
    vectors = []
    for n in range(-nn//2, nn//2+1):
        # C(n) = Intgr 0 -> 1 (f(t)e**(-n*2pi*i*t))
        # Finding magnitude and initial angle of the vector
        c = sum([(e**complex(0, -2*pi*n*t))
                * drawFromTXT(t) for t in np.linspace(0, 1, steps)])

        vectors.append(Vector(frequency=n, scale=scale, c=c))

    vectors = sorted(vectors, key=lambda v: -(v.c.real**2 + v.c.imag**2))
    return vectors

# A random setup for the vector
# vectors = [
#     Vector(frequency=i, scale=150, c=complex(1/i, 0)*e**complex(0, random()*2*pi)) for i in range(1, 50)
# ]

points = np.array([[0, 0]])
t = 0

def main_loop(dt, drawing, vectors, speed):
    window.clear()
    global t, points

    t += speed * dt

    for i, vector in enumerate(vectors):
        if i == 0:
            vector.update(t)
        else:
            vector.update(t, vectors[i-1].p)

        vector.draw()

    points = np.vstack([points, [[vectors[-1].x, vectors[-1].y]]])
    
    # On some setups GL_LINE_STRIP will throw an error, idk yet what it is causing it, in the meantime here it is a simple fix
    try:
        pyglet.graphics.draw(len(points)-1, pyglet.gl.GL_LINE_STRIP, ('v2f', (points[1:] + np.array([WIDHT/2, HEIGHT/2])).flatten()))
    except:
        pyglet.graphics.draw(len(points)-1, pyglet.gl.GL_POINTS, ('v2f', (points[1:] + np.array([WIDHT/2, HEIGHT/2])).flatten()))


if __name__ == "__main__":
    FPS = 60
    WSIZE = WIDHT, HEIGHT = (800, 800)
    FILENAME = "./img.txt"
    N_VECTORS = 200
    SCALE = 0.5
    SPEED = 0.05

    drawing = importTXT(FILENAME)
    vectors = init_vectors(nn=N_VECTORS, steps=1000, scale=SCALE)

    window = pyglet.window.Window(WIDHT, HEIGHT)
    pyglet.clock.schedule_interval(main_loop, 1/FPS, drawing, vectors, SPEED)
    pyglet.app.run()
