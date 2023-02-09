import pygame
from threading import Thread
from time import sleep
import pygame
import sys
import mouse
import keyboard
import PySimpleGUI as sg
import math


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
DEADZONE = 0.02
INPUT_DELAY = 0.002

class Converter(Thread):
    def __init__(self, scale):
        pygame.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.controller = self.joystick.get_name()
        self.motion = [0,0]
        self.scale = scale
    
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN: 
                if event.button == BUTTON_L_BUMPER:
                    if keyboard.is_pressed(['alt' , 'tab']):
                        keyboard.release(['alt' , 'tab'])
                    else:
                        keyboard.press(['alt' , 'tab'])
                elif event.button == BUTTON_R_BUMPER:
                    keyboard.press_and_release(['ctrl' , 'tab'])
                elif event.button == BUTTON_A:
                    mouse.click()
                elif event.button == BUTTON_B:
                    mouse.right_click()  
                elif event.button == BUTTON_R_STICK:
                    if mouse.is_pressed():
                        mouse.release()
                    else:
                        mouse.press() 
                
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis < 2:            
                    x_axis, y_axis = self.joystick.get_axis(0), self.joystick.get_axis(1)
                elif event.axis < 4:
                    x_axis, y_axis = self.joystick.get_axis(2), self.joystick.get_axis(3)
                else: # L, R trigger is also AXISMOTION
                    return


                # angle and magnitude of joystick movement
                angle = math.atan2(y_axis, x_axis)
                magnitude = math.sqrt(x_axis**2 + y_axis**2)

                # velocity in x and y directions
                velocity_x = magnitude * math.cos(angle)
                velocity_y = magnitude * math.sin(angle)

                self.motion[0] = velocity_x * self.scale ** 2
                self.motion[1] = velocity_y * self.scale ** 2
                

            elif event.type == pygame.JOYHATMOTION:
                if event.value == (-1, 0): 
                    keyboard.press_and_release("left")
                if event.value == (0, -1): 
                    keyboard.press_and_release("down")
                if event.value == (1, 0): 
                    keyboard.press_and_release("right")
                if event.value == (0, 1): 
                    keyboard.press_and_release("up")
            
        mouse.move(self.motion[0] , self.motion[1], absolute=False)
        sleep(INPUT_DELAY)


    def quit(self):
        pygame.quit()