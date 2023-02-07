import PySimpleGUI as sg
import keyboard
import sys


SCREEN_HEIGHT = 200
SCREEN_WIDTH = 200


font=('Arial', 16)


class GUI():
    def __init__(self, controller, scale = 2, font=('Arial', 16)):
        self.shift_on = False

        scale_layout = [[sg.Text('Controller: ' + controller, key='CONTROLLER')],
          [sg.Text('Pointer Speed: ' + str(scale), key='SCALE')], 
          [sg.Button('↑', key='SCALE_UP', button_color=('black', 'white'), size=(3, 2)),
           sg.Button('↓', key='SCALE_DOWN', button_color=('black', 'white'), size=(3, 2))],
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
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in 'QWERTYUIOP}{'] ,
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in'ASDFGHJKL:"'] 
            + [sg.Button('Enter', key='ENTER2', size=(6, 2), font=font)],            
            [sg.Button('Shift', key='SHIFT2', size=(4, 2), font=font)] + 
            [sg.Button(c, key=c, size=(3, 2), font=font) for c in 'ZXCVBNM<>?'] + 
            [sg.Button('Space', key='SPACE2', size=(5, 2), font=font)] 
            ]

        layout = [[sg.Column(scale_layout, key='SCALE_LAYOUT'),
                sg.Column(keyboard_layout, visible=True, key='KEYBOARD_LAYOUT'),
                sg.Column(keyboard_layout_shift, visible=False, key='KEYBOARD_LAYOUT_SHIFT')]]

        self.window = sg.Window('Controller_Mouse', layout, element_padding=(1, 1), keep_on_top=True,)
        self.scale = scale
        

    def run(self):
        while True:
            event, values = self.window.read(timeout=0)
            if event == sg.WIN_CLOSED:
                break
            elif event == 'SCALE_UP'and self.scale < 4:
                self.scale += 0.5
            elif event == 'SCALE_DOWN' and self.scale > 1.5:
                self.scale -= 0.5
                
            elif event == "SHIFT" or event == "SHIFT2":
                print("SHIFT")
                if self.shift_on:
                    self.window['KEYBOARD_LAYOUT_SHIFT'].update(visible=False)
                    self.window['KEYBOARD_LAYOUT'].update(visible=True)
                    self.shift_on = False
                    print(self.shift_on)
                else:
                    self.window['KEYBOARD_LAYOUT'].update(visible=False)
                    self.window['KEYBOARD_LAYOUT_SHIFT'].update(visible=True)
                    self.shift_on = True
                    print(self.shift_on)
            elif event == "BACK" or event == "BACK":
                keyboard.press_and_release('back')
            elif event == "ENTER" or event == "ENTER2":
                keyboard.press_and_release('enter')
            elif event == "SPACE" or event == "SPACE2":
                keyboard.press_and_release('space')

            elif event.isalpha():
                print(event)
            # elif event is not None:
            #     print(event)
            #     keyboard.press_and_release(event)
            self.window['SCALE'].update('Speed(1.5 ~ 4): {}'.format(self.scale))

        self.window.Close()
    

if __name__ == '__main__':
    app = GUI("xbox controller", 2)
    app.run()