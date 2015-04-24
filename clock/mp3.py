__author__ = 'Victor'

import mp3play
import time

def mp3(playtime=30, music_file=r'E:\music\clock.mp3'):
    clip = mp3play.load(music_file)
    clip.play()

    time.sleep(min(playtime, clip.seconds()))
    clip.stop()
    return 0