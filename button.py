import pygame

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