import pygame
from player import Player
from Text import Text
import random

class Button(pygame.sprite.Sprite):
  def __init__(self,screen, image, scale, x, y):
    pygame.sprite.Sprite.__init__(self)
    width = image.get_width()
    height = image.get_height()
    self.image = pygame.transform.scale(image, (scale*width, scale*height))
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
    self.clicked = False
    self.screen = screen
    self.scale = scale
    self.x = x
    self.y = y

  def draw(self):
    self.screen.blit(self.image, (self.rect.x, self.rect.y)) #blit = draws sprite on the screen
    mousepos = pygame.mouse.get_pos()
    pressed = False
    if self.rect.collidepoint(mousepos):#check if mouse is overlapping with sprite
      
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        print("clicked")
        self.clicked = True
        pressed = True
    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False
    return pressed
  
class UpgradeButton(Button):
  def __init__(self,screen, scale, x, y,type: str):
    self.health_increase = 25
    self.dmg_increase = 5
    self.speed_increase = 0.05
    self.fire_rate = 5
    self.frequency_barrier = 500

    self.type = type
    self.info = {}
    self.generate_info()
    Button.__init__(self,screen, self.info[self.type]["image"], scale, x, y)

  def generate_info(self):
    
    self.info = {
      "hp" : {
        "image" :pygame.image.load("assets/HP.png"),
        "message" : "Increase hp by " + str(self.health_increase)
      },
      "dmg" : {
        "image" : pygame.image.load("assets/DMG.png"),
        "message" : "Increase dmg by " + str(self.dmg_increase)

      },
      "speed" : {
        "image" : pygame.image.load("assets/SPEED.png"),
        "message" : "Increase speed by "+ str(round(self.speed_increase, 2))

      },
      "barrier" : {
        "image" : pygame.image.load("assets/barrier.png"),
        "message": "Unlock the barrier ability"
      },
      "fire rate" : {
        "image" : pygame.image.load("assets/fr.png"),
        "message": "Increase Fire Rate"
      }, 
      "barrier amount" : {
        "image" : pygame.image.load("assets/barrier amount.png"),
        "message": "Increase Barrier Amount by 1"
      }, 
      "barrier speed" : {
        "image" : pygame.image.load("assets/barrier speed.png"),
        "message": "Increase Barrier Speed"
      }, 

    }

  def draw(self):
    text = Text(self.screen, self.info[self.type]["message"], 20, (0, 0, 0), self.rect.x + 50, self.rect.y + 150)
    text.draw()
    return Button.draw(self)

  def checker(self, player: Player, button_types):
    if self.type == "hp":
      player.upgrade_health(self.health_increase)
      self.health_increase += 10
    elif self.type == "dmg":
      player.upgrade_damage(self.dmg_increase)
      self.dmg_increase += 1
    elif self.type == "speed":
      player.upgrade_speed(self.speed_increase)
      self.speed_increase += 0.05
    elif self.type == "fire rate":
      player.upgrade_firerate(self.fire_rate)
      self.fire_rate += 5
    elif self.type == "barrier":
      player.has_barrier = True
    elif self.type == "barrier amount":
      player.barrier_size += 1
    elif self.type == "barrier speed":
      player.burst_cooldown -= self.frequency_barrier
    

    # Change the button's type

    while True:
      random_type = random.choice(list(self.info.keys()))
      if random_type == "barrier" and player.has_barrier:
        continue
      # If this type is not currently an upgrade button
      if random_type not in button_types:
        if not player.has_barrier and random_type in ("barrier amount", "barrier speed"):
          continue
        self.type = random_type
        Button.__init__(self,self.screen, self.info[self.type]["image"], self.scale, self.x, self.y)

        break

    # Increases threshold to get next upgrade  
    player.increase_level()
    # Updates dictionary with new upgrade stats
    self.generate_info()