from threading import Thread
import mouse
from time import sleep


DELAY = 0.01
class Worker(Thread):
    def __init__(self):
        super().__init__()
        self.dx = 0
        self.dy = 0
        self.go_on = True
    
    def run(self):
        while self.go_on:
            move(self.dx, self.dy)
            sleep(DELAY)


def move(dx, dy):
    x, y = mouse.get_position()
    x += dx
    y += dy
    mouse.move(x, y)