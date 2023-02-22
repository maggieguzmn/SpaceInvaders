import sys
from time import sleep

import pygame

from bullet import Bullet
from superbullet import SuperBullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets, superbullets):
    """Respond to keypresses."""
    button = event.key if event.type == pygame.KEYDOWN else event.button
    if button == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    elif button == pygame.K_LEFT:
        # Move the ship to the left.
        ship.moving_left = True
    elif button == pygame.K_SPACE or button == pygame.BUTTON_LEFT:
        fire_bullet(ai_settings, screen, ship, bullets)
        #print("pew", event)
    elif button == pygame.K_x or button == pygame.BUTTON_RIGHT:
        fire_superbullet(ai_settings, screen, ship, superbullets)
    elif button == pygame.K_q:
        sys.exit()
    elif button == pygame.K_ESCAPE:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def fire_superbullet(ai_settings, screen, ship, superbullets): #Correct this so it takes things from parent class bullets
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(superbullets) < ai_settings.superbullets_allowed and ai_settings.superbullets_limit > 0:
        new_superbullet = SuperBullet(ai_settings, screen, ship)
        superbullets.add(new_superbullet)
        ai_settings.superbullets_limit -= 1

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # Move the ship to the left.
        ship.moving_left = False    


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, superbullets):
    """Respond to keypress and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and not stats.game_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
            aliens, bullets, superbullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, superbullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
aliens, bullets, superbullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse curson.
        pygame.mouse.set_visible(False)        
        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        superbullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, superbullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ships and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for superbullet in superbullets.sprites():
        superbullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, superbullets):
    """"Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    superbullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)  

    for superbullet in superbullets.copy():
        if superbullet.rect.bottom <= 0:
            superbullets.remove(superbullet) 
    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, superbullets)
    
    
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, 
ship, aliens, bullets, superbullets):
    """Respond to bullet-alien collisions."""
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullets and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    collisions2 = pygame.sprite.groupcollide(superbullets, aliens, False, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

    if collisions2:
        for aliens in collisions2.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

    if collisions or collisions2:
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

                # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)



def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Create an alien and find the number of aliens in a row.
    #Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings= ai_settings, screen=screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create an alien and find the number of aliens in a row.
    #Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings= ai_settings, screen=screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Renspond appropiately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1    

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, superbullets):
    """Respond to ship being hit by an alien."""
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1 
        #print(stats.ships_left)

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        superbullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, superbullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as ship got hit.
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, superbullets)
            break

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, superbullets):
    """
    Check if the fleet is at an edge, and then
    ppdate the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, superbullets)
    
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, superbullets)

def check_high_score(stats, sb):
    """Check to see if there is a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()