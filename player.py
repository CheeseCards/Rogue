import pygame

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, hp):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.Surface((17,17))
      self.image.fill((255,255,255))
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
      self.hp = hp
      
      self.score = 0
    
  def update(self):
    speed = 3
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_w]:
      self.rect.y -= speed
    if key_pressed[pygame.K_s]:
      self.rect.y += speed
    if key_pressed[pygame.K_a]:
      self.rect.x -= speed
    if key_pressed[pygame.K_d]:
      self.rect.x += speed
  def shoot(self):
    bullet = Bullet(self)
    return bullet

class Enemy(pygame.sprite.Sprite):
   def __init__(self, x, y):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.Surface((17,17))
      self.image.fill((255, 61, 3))
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
      self.speed = 2
    
   def update(self, player):
    enemy_vector = pygame.Vector2(self.rect.center)
    player_vector = pygame.Vector2(player.rect.center)
    if player_vector == enemy_vector:
      return
    direction = (player_vector - enemy_vector).normalize() * self.speed
    self.rect.center += direction

class Bullet(pygame.sprite.Sprite):
  def __init__(self, player):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((17,17))
    self.image.fill((128, 115, 46))
    self.rect = self.image.get_rect()
    self.rect.x = player.rect.x
    self.rect.y = player.rect.y
    self.speed = 1
  def update(self):
    self.speed += 0.01
    bullet_vector = pygame.Vector2(self.rect.center)
    mouse_vector = pygame.Vector2(pygame.mouse.get_pos())
    if bullet_vector == mouse_vector:
      return
    direction = (mouse_vector - bullet_vector).normalize() * self.speed
    self.rect.center += direction


  
