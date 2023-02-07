from threading import Thread
from time import sleep
import pygame
import sys
import mouse
import keyboard
import PySimpleGUI as sg
import math

# 할꺼 
# 알트탭(구현), 방향키(구현), 컨트롤탭(구현), 움직임(어느정도 됨), 가상키보드 구현하면 끝 

# Constants
BUTTON_START = 7
BUTTON_SELECT = 6
BUTTON_R_BUMPER = 5
BUTTON_L_BUMPER = 4
BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3
BUTTON_R_STICK = 9
BUTTON_L_STICK = 8
SCREEN_HEIGHT = 300
SCREEN_WIDTH = 200
DEADZONE = 0.02

scale = 2
motion=[0,0]


# initialize pygame
pygame.init()

# get joystick(controller)
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
controller = joysticks[0].get_name()

# GUI
sg.theme('DarkBlue')
layout = [[sg.Text('Controller: ' + controller, key='CONTROLLER')],
          [sg.Text('Pointer Speed: ' + str(scale), key='SCALE')], 
          [sg.Button('↑', key='UP', button_color=('black', 'white'), size=(3, 2)),
           sg.Button('↓', key='DOWN', button_color=('black', 'white'), size=(3, 2))],
           [sg.Button('on-screen keyboard', key='keyboard')],
          ]
window = sg.Window('Controller_Mouse', layout, size=(SCREEN_HEIGHT, SCREEN_WIDTH))



running = True
while running:

    event, values = window.read(timeout=0) 
    if event == 'close' or event == sg.WIN_CLOSED:
        running = False
    elif event == 'UP'and scale < 4:
        scale += 0.5
    elif event == 'DOWN' and scale > 1.5:
        scale -= 0.5
    window['SCALE'].update('Speed(1.5 ~ 4): {}'.format(scale))
    

    if abs(motion[0]) < DEADZONE:
        motion[0] = 0
    if abs(motion[1]) < DEADZONE:
        motion[1] = 0
    mouse.move(motion[0] , motion[1], absolute=False)


    
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.JOYBUTTONDOWN: 
            if event.button == BUTTON_START:
                window.bring_to_front()
            if event.button == BUTTON_L_BUMPER:
                if keyboard.is_pressed(['alt' , 'tab']):
                    keyboard.release(['alt' , 'tab'])
                else:
                    keyboard.press(['alt' , 'tab'])
            if event.button == BUTTON_R_BUMPER:
                keyboard.press_and_release(['ctrl' , 'tab'])
            if event.button == BUTTON_X:
                mouse.click()
            if event.button == BUTTON_A:
                mouse.right_click()  
            if event.button == BUTTON_R_STICK:
                if mouse.is_pressed():
                    mouse.release()
                else:
                    mouse.press() 

        elif event.type == pygame.JOYAXISMOTION:
            if event.axis < 2:            
                x_axis, y_axis = joysticks[0].get_axis(0), joysticks[0].get_axis(1)
            elif event.axis < 4:
                x_axis, y_axis = joysticks[0].get_axis(2), joysticks[0].get_axis(3)

            # angle and magnitude of joystick movement
            angle = math.atan2(y_axis, x_axis)
            magnitude = math.sqrt(x_axis**2 + y_axis**2)

            # velocity in the x and y directions
            velocity_x = magnitude * math.cos(angle)
            velocity_y = magnitude * math.sin(angle)

            motion[0] = velocity_x * scale ** 2
            motion[1] = velocity_y * scale ** 2

        elif event.type == pygame.JOYHATMOTION:
            if event.value == (-1, 0): 
                keyboard.press_and_release("left")
            if event.value == (0, -1): 
                keyboard.press_and_release("down")
            if event.value == (1, 0): 
                keyboard.press_and_release("right")
            if event.value == (0, 1): 
                keyboard.press_and_release("up")

pygame.quit()
print('bye')
sys.exit()



