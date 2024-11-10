import pygame
import random


class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, hp,dmg, bullet_group, screen_height, screen_width):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.Surface((17,17))
      self.image.fill((255,255,255))
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
      self.screen_height = screen_height
      self.screen_width = screen_width
      # Player stats
      self.hp = hp
      self.dmg = dmg
      self.score = 0
      self.speed = 3
    
      self.next_level = 5 # Score upgrade threshold

      # Player abilities
      self.has_barrier = False
      self.barrier_size = 5
      self.last_burst = 0
      self.burst_cooldown = 5000
      
      self.shoot_cooldown = 60
      self.bullet_group = bullet_group

  def increase_level(self):
    self.next_level = int(self.next_level * 1.5)

  def generate_barrier(self):
    barrier_amount = 0
    while barrier_amount < self.barrier_size:
      bullet = Bullet(self, False, (213, 192, 25))
      self.bullet_group.add(bullet)
      barrier_amount += 1


  def update(self):
    if self.has_barrier and pygame.time.get_ticks() - self.last_burst >= self.burst_cooldown:
      self.last_burst = pygame.time.get_ticks()
      self.generate_barrier()

    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_w]:
      self.rect.y -= self.speed
    if key_pressed[pygame.K_s]:
      self.rect.y += self.speed
    if key_pressed[pygame.K_a]:
      self.rect.x -= self.speed
    if key_pressed[pygame.K_d]:
      self.rect.x += self.speed
    if self.rect.x > self.screen_width:
      self.rect.x = 0
    elif self.rect.x < 0:
      self.rect.x = self.screen_width
    if self.rect.y < 0:
      self.rect.y = self.screen_height
    elif self.rect.y > self.screen_height:
      self.rect.y = 0
    
  def shoot(self):
    bullet = Bullet(self)
    return bullet
    
  def upgrade_health(self, amount):
    self.hp += amount
  def upgrade_speed(self, amount):
    self.speed += amount
  def upgrade_damage(self, amount):
    self.dmg += amount
  def upgrade_firerate(self, amount):
    self.shoot_cooldown -= amount

class Enemy(pygame.sprite.Sprite):
  def __init__(self, screen_width, screen_height, size, hp):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((size, size))
    self.image.fill((255, 61, 3))
    self.rect = self.image.get_rect()
    self.speed = 2
    self.hp = hp
    self.random_position(screen_width, screen_height)
    self.enemy_points = 1 + (self.hp // 10)

  def random_position(self, width, height):
    # Generate random position
    x = 0
    y = 0
    if random.randint(0,1) == 1:
      x = random.randint(0, int(width/4))
    else:
      x = random.randint(int(width/4*3), width)
    if random.randint(0,1) == 1:
      y = random.randint(0, int(height/4))
    else:
      y = random.randint(int(height/4*3), height)
    
    # Set the enemy position to the random values
    self.rect.x = x
    self.rect.y = y
    
  def update(self, player):
    enemy_vector = pygame.Vector2(self.rect.center)
    player_vector = pygame.Vector2(player.rect.center)
    if player_vector == enemy_vector:
      return
    direction = (player_vector - enemy_vector).normalize() * self.speed
    self.rect.center += direction

class Bullet(pygame.sprite.Sprite):
  def __init__(self, player, follows_mouse = True, color = (128, 115, 46)):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((17,17))
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.x = player.rect.x
    self.rect.y = player.rect.y
    self.speed = 1
    self.follows_mouse = follows_mouse
    self.direction = [random.uniform(-2, 2), random.uniform(-2, 2)]
  def update(self):
    if self.follows_mouse == True:
      self.speed += 0.01
      bullet_vector = pygame.Vector2(self.rect.center)
      mouse_vector = pygame.Vector2(pygame.mouse.get_pos())
      if bullet_vector == mouse_vector:
        return
      direction = (mouse_vector - bullet_vector).normalize() * self.speed
      self.rect.center += direction

    else: # Shoot bullet in random direction
      self.rect.x += self.direction[0] * self.speed
      self.rect.y += self.direction[1] * self.speed

  
