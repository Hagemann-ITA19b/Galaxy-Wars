import os


class Settings(object):
    window_height = 1080
    window_width = 1920
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_ships = os.path.join(path_file, "Ships")
    path_ui = os.path.join(path_file, "UI")
    path_ui_radar = os.path.join(path_ui, "radar")
    path_turrets = os.path.join(path_file, "Turrets")
    path_bullets = os.path.join(path_file, "Bullets")
    path_starfighters = os.path.join(path_file, "Starfighters")
    path_assault = os.path.join(path_ships, "assault")
    path_carrier = os.path.join(path_ships, "carrier")
    path_dreadnought = os.path.join(path_ships, "dreadnought")
    path_spacestation = os.path.join(path_file, "spacestations")
    turret_size = (10,10)
    bullet_size = (10, 10)
    starfighter_size = (30, 30)
    title = "Galaxy Wars"