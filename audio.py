import os
import pygame
from pygame import mixer
from settings import Settings

class Audio():
    def __init__(self) -> None:
        mixer.init()
        self.currently_playing = None
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
    


    def play_music(self, audio):
        if mixer.music.get_busy() == False:
            mixer.music.load(os.path.join(Settings.path_soundtrack, audio))
            mixer.music.set_volume(0.05)
            mixer.music.play()
            self.currently_playing = audio
            print("!")
        elif self.currently_playing != audio:
            mixer.music.fadeout(1000)

            