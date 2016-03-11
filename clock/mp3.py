__author__ = 'Victor'

import time
import pygame

def mp3(playtime=30, music_file=r'clock.mp3'):
    pygame.mixer.init()
    pygame.mixer.music.load("clock.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    return 0

if __name__ == "__main__":
    mp3()