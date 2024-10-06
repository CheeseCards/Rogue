import pygame
from Text import Text
from button import Button
from player import Player, Enemy
pygame.init()
enemy_group = pygame.sprite.Group()
enemy1 = Enemy(50, 50)
enemy2 = Enemy(100, 100)
enemy3 = Enemy(200, 200)
enemy_group.add([enemy1, enemy2, enemy3])
player = Player(250, 250, 100)
player_group = pygame.sprite.Group()
player_group.add(player)
screen_width = 500
screen_height = 500
bullet_group = pygame.sprite.Group()
clock = pygame.time.Clock() # Keeps track of how fast the game is running
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("pew pew")
frames = 0
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    player_group.draw(screen)
    enemy_group.draw(screen)
    enemy_group.update(player)  
    bullet_group.update()
    bullet_group.draw(screen)
    player_group.update()
    hp = Text(screen, "HP:" + str(player.hp), 12, (255,255,255), screen_width/2, screen_height/5)
    score = Text(screen, "SCORE:" + str(player.score), 12,(128, 255, 40), screen_width/2, screen_height/10)
    hp.draw()
    score.draw()
    frames += 1
    if frames >= 60:
        bullet = player.shoot()
        bullet_group.add(bullet)
        frames = 0
    bullet_hit = pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)
    for bullet in bullet_hit:
        enemy = Enemy(0,0)
        enemy_group.add(enemy)
        player.score += 1
    enemy_hit = pygame.sprite.spritecollide(player, enemy_group, False)
    for enemy in enemy_hit:
        player.hp -= 10
    pygame.display.update()
    clock.tick(60)
  
        