import PySimpleGUI as sg
import keyboard
from pywinauto import Desktop, Application
from time import sleep
from pywinauto import Desktop, Application
from threading import Thread


SCREEN_HEIGHT = 200
SCREEN_WIDTH = 200




class GUI(Thread):
    def __init__(self, converter , font=('Arial', 16)):
        scale_layout = [[sg.Text('Controller: ' + converter.controller, key='CONTROLLER')],
          [sg.Text('Speed(1.5 ~ 4): ' + str(converter.scale), key='SCALE')], 
          [sg.Button('↑', key='SCALE_UP', button_color=('black', 'white'), size=(3, 2)),
           sg.Button('↓', key='SCALE_DOWN', button_color=('black', 'white'), size=(3, 2))],
           [sg.Text('LStick: mouse\nRStick: mouse drag\nLBumper: alt + tab\nRBumper: ctrl + tab\nA: click\nB: right click', key='KEYBIND')], 
          ]
        
        keyboard_layout = [
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in '1234567890-='] 
            + [sg.Button('⌫', key='BACK', size=(3, 2), font=font)],            
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in 'qwertyuiop[]'] ,
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in 'asdfghjkl;\''] 
            + [sg.Button('Enter', key='ENTER', size=(6, 2), font=font)],            
            [sg.Button('Shift', key='SHIFT', size=(4, 2), font=font)] + 
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in 'zxcvbnm,./']+ 
            [sg.Button('Space', key='SPACE', size=(5, 2), font=font)] 
            ]

        keyboard_layout_shift = [
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in '!@#$%^&*()_+'] 
            + [sg.Button('⌫', key='BACK2', size=(3, 2), font=font)],            
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in 'QWERTYUIOP{}'] ,
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in'ASDFGHJKL:"'] 
            + [sg.Button('Enter', key='ENTER2', size=(6, 2), font=font)],            
            [sg.Button('Shift', key='SHIFT2', size=(4, 2), font=font)] + 
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in 'ZXCVBNM<>?'] + 
            [sg.Button('Space', key='SPACE2', size=(5, 2), font=font)] 
            ]

        layout = [[sg.Column(scale_layout, key='SCALE_LAYOUT'),
                sg.Column(keyboard_layout, visible=True, key='KEYBOARD_LAYOUT'),
                sg.Column(keyboard_layout_shift, visible=False, key='KEYBOARD_LAYOUT_SHIFT')]]
        
        self.window = sg.Window('Controller_Mouse', layout, element_padding=(1, 1), 
                                grab_anywhere=True, keep_on_top=True, alpha_channel=1,
                                location=(500,500), finalize=True,

                                )
        
        self.shift_on = False
        self.converter = converter

    def write(self, event):
        windows = Desktop(backend="uia").windows()
        for window in windows:
            if window.window_text() != 'Controller_Mouse' and window.window_text() != '작업 표시줄':
                window.set_focus()
                keyboard.write(event)
                break
    
    def press(self, event):
        windows = Desktop(backend="uia").windows()
        for window in windows:
            if window.window_text() != 'Controller_Mouse' and window.window_text() != '작업 표시줄':
                window.set_focus()
                keyboard.press_and_release(event)
                break
    
    def close(self):
        self.window.close()

    def run(self):
    
        event, values = self.window.read(timeout=0)
        if event == sg.WIN_CLOSED:
            return False
        elif event == 'SCALE_UP'and self.converter.scale < 4:
            self.converter.scale += 0.5
            self.window['SCALE'].update('Speed(1.5 ~ 4): {}'.format(self.converter.scale))

        elif event == 'SCALE_DOWN' and self.converter.scale > 1.5:
            self.converter.scale -= 0.5
            self.window['SCALE'].update('Speed(1.5 ~ 4): {}'.format(self.converter.scale))
            
        elif event == "SHIFT" or event == "SHIFT2":
            if self.shift_on:
                self.window['KEYBOARD_LAYOUT_SHIFT'].update(visible=False)
                self.window['KEYBOARD_LAYOUT'].update(visible=True)
                self.shift_on = False
            else:
                self.window['KEYBOARD_LAYOUT'].update(visible=False)
                self.window['KEYBOARD_LAYOUT_SHIFT'].update(visible=True)
                self.shift_on = True

        elif event == "BACK" or event == "BACK2":
            self.press('backspace')
        elif event == "ENTER" or event == "ENTER2":
            self.press('enter')
        elif event == "SPACE" or event == "SPACE2":
            self.write(' ')

        elif event != '__TIMEOUT__':
            self.write(event)
    


if __name__ == '__main__':
    app = GUI("xbox controller", 2)

    
    while True:
        if app.run() == False:
            break

    app.close()
 