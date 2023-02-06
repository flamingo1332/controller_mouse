from threading import Thread
from time import sleep
import pygame
import pyautogui
import mouse
import keyboard
from button import Button
from worker import Worker

SCREEN_HEIGHT = 300
SCREEN_WIDTH = 400
DEADZONE = 0.25
velocity = 4


def show_text( msg, color, x=50, y=50 ):
    text = font.render( msg, True, color)
    screen.blit(text, ( x, y ))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mouse Controller')

up_image = pygame.image.load('img/up.png').convert_alpha()
down_image = pygame.image.load('img/down.png').convert_alpha()

up_button = Button(100, 200, up_image, 0.2)
down_button = Button(200, 200, down_image, 0.2)

pygame.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

text_surface = font.render('Some Text', False, (0, 0, 0))
screen.blit(text_surface, (50,50))


worker = Worker()
worker.start()


print('Controller :')
joysticks = []
joysticks.append(pygame.joystick.Joystick(0))

running = True
while running:

    screen.blit(text_surface, (50,50))
    screen.fill((255,255,255))
    
    # velocity
    if up_button.draw(screen): 
        velocity += .5
        velocity = round(velocity, 1)
        
        
    elif down_button.draw(screen): 
        velocity -= .5
        velocity = round(velocity, 1)
        

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print(event.button)
            if event.button in (0, 7, 8, 9, 10):
                print(event.button)
                print("click")
                mouse.click()
            elif event.button == 11:
                print(event.button)
                keyboard.press_and_release('up')
            elif event.button == 12:
                print(event.button)
                keyboard.press_and_release('down')
            elif event.button == 13:
                print(event.button)
                keyboard.press_and_release('left')
            elif event.button == 14:
                print(event.button)
                keyboard.press_and_release('right')
            else:
                print(event.button)
                print("other")
        elif event.type == pygame.QUIT:
            running=False

        elif event.type == pygame.JOYAXISMOTION:
            axis, value = event.axis, event.value
            print(axis)
            # print('    ' * (axis + 1), value)
            value = value ** 3 * abs(value) ** 1
            value *= velocity
            if axis in (0, 2):
                if abs(value) < DEADZONE:
                    worker.dx = 0
                else:
                    worker.dx = value
            if axis in (1, 3):
                if abs(value) < DEADZONE:
                    worker.dy = 0
                else:
                    worker.dy = value

        # print(worker.dx, '\t', worker.dy)
    
    show_text("Velocity: " + str(velocity), (0,0,0))
    pygame.display.update()

worker.go_on = False
worker.join()
pygame.quit()
print('bye')



