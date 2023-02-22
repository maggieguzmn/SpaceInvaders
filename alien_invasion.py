import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # Initialize game and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    superbullets = Group()
    aliens = Group()

    # Create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game.
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, superbullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, superbullets) 
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, superbullets)
        gf.update_screen(ai_settings = ai_settings, screen = screen, stats= stats, sb = sb, ship = ship, aliens = aliens, bullets = bullets, superbullets= superbullets, play_button = play_button)
run_game()