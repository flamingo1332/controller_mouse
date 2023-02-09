from threading import Thread
from time import sleep
import sys
import PySimpleGUI as sg
from gui import GUI
from converter import Converter


INITIAL_SCALE = 2


def main():    
    converter = Converter(INITIAL_SCALE)
    gui = GUI(converter)

    while True:
        if gui.run() == False:
            break
        converter.run()

    gui.close()
    converter.quit()
    print('bye')
    sys.exit()


main()


