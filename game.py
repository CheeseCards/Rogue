import pygame
from Text import Text 
from button import Button, UpgradeButton
from player import Player, Enemy

paused = False
upgrading = False
screen_width = 1500
screen_height = 800
clock = pygame.time.Clock() # Keeps track of how fast the game is running
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("pew pew")
frames = 0
time_elapse = 0
next_boss_spawn = 600

pygame.init()

# Sprite groups
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
upgrade_group = pygame.sprite.Group()
# Generate playerte
player = Player(250, 250, hp=100, dmg=10, bullet_group=bullet_group, screen_height = screen_height, screen_width = screen_width)
player_group.add(player)

# Generate buttons
button_img = pygame.image.load("assets/pause.png")
pause_button = Button(screen, button_img, 0.05, 20,20)
upgrade1 = UpgradeButton(screen,0.5, 300, 300, "hp")
upgrade2 = UpgradeButton(screen,0.5, 750, 300, "dmg")
upgrade3 = UpgradeButton(screen,0.5, 1200, 300, "speed")
upgrade_group.add([upgrade1, upgrade2, upgrade3])

def generate_enemy(size=15, hp=10):
    enemy = Enemy(screen_width, screen_height, size=size, hp=hp)
    enemy_group.add(enemy)

# Generates 3 enemies
for i in range(3):
    generate_enemy()

# Game loop
while True:
    screen.fill((125, 125, 125))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # Draw sprite groups
    player_group.draw(screen)
    enemy_group.draw(screen)
    bullet_group.draw(screen)

    # Check if game is paused
    if not paused:
        # Update sprite groups
        enemy_group.update(player)  
        bullet_group.update()
        player_group.update()

        
        time_elapse += 1
        
        # Automatic bullet shooting
        if frames >= player.shoot_cooldown:
            bullet = player.shoot()
            bullet_group.add(bullet)
            frames = 0

        if time_elapse >= next_boss_spawn:
            generate_enemy(size = 30, hp = 100)
            next_boss_spawn += 600
            
        
        frames += 1
    elif upgrading == True:
        #                   "HP"            "DMG"         "Speed"
        button_types = [upgrade1.type, upgrade2.type, upgrade3.type]
        if upgrade1.draw():
            upgrading, paused = False, False
            generate_enemy()
            upgrade1.checker(player, button_types)
        if  upgrade2.draw():
            upgrading, paused = False, False
            generate_enemy()
            upgrade2.checker(player, button_types)
        if  upgrade3.draw():
            upgrading, paused = False, False
            generate_enemy()
            upgrade3.checker(player, button_types)
    if player.score >= player.next_level:
        upgrading = True
        paused = True



    # Draw text elements
    hp = Text(screen, "HP:" + str(player.hp), 12, (255,255,255), screen_width/2, 100)
    score = Text(screen, "SCORE:" + str(player.score), 12,(128, 255, 40), screen_width/2, screen_height/10)
    time = Text(screen, "Timer:" + str(round(time_elapse/60, 2)), 12, (255,255,255), screen_width/2, screen_height/15)
    upgrade = Text(screen, "Next Upgrade:" + str(round(player.next_level)), 12, (255,255,255), screen_width/2, 120)
    hp.draw()
    score.draw()
    time.draw()
    upgrade.draw()

    # Draw buttons
    if pause_button.draw(): # If we pressed the pause button
        paused = not paused

    bullet_hit = pygame.sprite.groupcollide(bullet_group, enemy_group, True, False)
    for bullet in bullet_hit:
        for enemy in bullet_hit[bullet]: # This enemy has been touched by a bullet
            # Enemy takes damaged
            enemy.hp -= player.dmg
            if enemy.hp <= 0:
                enemy_group.remove(enemy)
                enemy = Enemy(screen_width, screen_height, size=15+int(player.score/15), hp=10+player.score)
                enemy_group.add(enemy)
                player.score += enemy.enemy_points
                
    enemy_hit = pygame.sprite.spritecollide(player, enemy_group, False)
    for enemy in enemy_hit:
        player.hp -= 10
    if player.hp <= 0:
        quit()
    pygame.display.update()
    clock.tick(60)
  
        