class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230) #background color

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.superbullets_allowed = 1
        self.superbullets_limit = 3
        self.superbullet_width = 300
        

        # Alien settings
        self.fleet_drop_speed = 20

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien values increase 
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""    
        self.ship_speed_factor = 1.1*0.5
        self.bullet_speed_factor = 1
        self.superbullet_speed_factor = 0.5
        self.alien_speed_factor = 0.25

        # Fleet direction 1 represents right; -1 represents lefts
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)