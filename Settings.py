import os

class Settings(object):
    window_height = 1080
    window_width = 1920
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_ships = os.path.join(path_file, "Ships")
    path_ui = os.path.join(path_file, "UI")
    path_turrets = os.path.join(path_file, "Turrets")
    path_bullets = os.path.join(path_file, "Bullets")
    player_size = (25, 25)
    bullet_size = (25, 25)
    title = "Galaxy Wars"