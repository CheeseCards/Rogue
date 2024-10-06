import pygame

class Text:
  def __init__(self,surface, text, size, color, x, y):
    self.surface = surface
    self.text = text
    self.size = size
    self.color = color
    self.x = x
    self.y = y
    font_name = pygame.font.match_font("arial")
    self.font = pygame.font.Font(font_name, self.size)
  def draw(self):
    text_surface = self.font.render(self.text, True, self.color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (self.x, self.y)
    self.surface.blit(text_surface, text_rect)