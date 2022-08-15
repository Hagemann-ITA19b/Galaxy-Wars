import os
import pygame
from pygame import mixer
from settings import Settings
from random import randint

class Audio():
    def __init__(self) -> None:
        mixer.init()
        self.currently_playing = None
        self.clock_time = pygame.time.get_ticks()
        self.tracklist = ["ambient-cyberpunk-cinematic-8411.mp3","cyberpunk-109354.mp3","danger-at-the-horizon-11758.mp3","danger-beats-113879.mp3"]
        self.intro = True
    # blaster_sound = pygame.mixer.Sound(os.path.join(Settings.path_image, "blaster.wav"))
    # blaster_sound.set_volume(0.01)

    # def play_sound(sound):
    #     busy3 = pygame.mixer.Channel(3).get_busy()
    #     busy1 = pygame.mixer.Channel(1).get_busy()
    #     if sound == "blaster":
    #         pygame.mixer.Channel(7).play(Sounds.blaster_sound)
    #     if sound == "refill":
    #         pygame.mixer.Channel(2).play(Sounds.refill_sound)
    #     if sound == "explosion":
    #         pygame.mixer.Channel(3).play(Sounds.explosion_sound)
    #     if sound == "shields_low":
    #         pygame.mixer.Channel(4).play(Sounds.shields_low)
    #     if sound == "tk_blast":
    #         pygame.mixer.Channel(5).play(Sounds.tk_blast)
    #     if sound == "empty":
    #         pygame.mixer.Channel(7).play(Sounds.empty_sound)
    #     if sound == "rocket":
    #         pygame.mixer.Channel(7).play(Sounds.rocket_sound)
    #     if sound == "player_hit":
    #         pygame.mixer.Channel(0).play(Sounds.player_hit)
    #     if sound == "jetpack":
    #         pygame.mixer.Channel(6).play(Sounds.jetpack_sound)
    #     if sound == "shield_hit":
    #         pygame.mixer.Channel(0).play(Sounds.shield_sound)
    #     if sound == "jetpack":
    #         pygame.mixer.Channel(0).play(Sounds.jetpack_sound)
    #     if sound == "ob_distant" and busy3 == False:
    #         pygame.mixer.Channel(3).play(Sounds.ob_distant)
    #         print("playing")
    #     if sound == "danger" and busy1 == False:
    #         pygame.mixer.Channel(1).play(Sounds.danger)
    

    def soundtrack(self):
        if self.intro == True:
            mixer.music.fadeout(500)
            self.intro = False
        if mixer.music.get_busy() == False:
            if pygame.time.get_ticks() > self.clock_time:
                self.clock_time = pygame.time.get_ticks() + 7200
                index = randint(0,len(self.tracklist)-1)
                self.play_music(self.tracklist[index])

    def play_music(self, audio):
        if mixer.music.get_busy() == False:
            mixer.music.load(os.path.join(Settings.path_soundtrack, audio))
            mixer.music.set_volume(0.03)
            mixer.music.play()
            self.currently_playing = audio
        elif self.currently_playing != audio:
            mixer.music.fadeout(100)

            