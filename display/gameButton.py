import pygame
import gameTest

#hex colors used
black = (0, 0, 0)
gray = (128, 128, 128)
light_gray = (192, 192, 192)


class gameButton():

    def __init__(self, x_pos, y_pos, width, height, title):
        self.x_pos = x_pos
        self.y_pos= y_pos
        self.title = title
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.surface = pygame.Surface((width, height))
        self.click = False
    
    def createButton(self):
        #creates the font
        font = pygame.font.SysFont(None, 24)
        
        #get the location of the mouse
        mouse = pygame.mouse.get_pos()
        
        #gets the font
        text = font.render(self.title, True, light_gray)
        
        #gets the coordinates for the text
        button_text = text.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))
        
        # if self.rect.collidepoint(mouse):
        #     pygame.draw.rect(self.surface, gray, self.rect)
        
        #creates the button
        pygame.draw.rect(self.surface, black, self.rect)
        
        #display text on button surface
        self.surface.blit(text, button_text)
        
        #displays the acatual button
        pygame.display.get_surface().blit(self.surface, (self.x_pos, self.y_pos))
        
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            print("mouse was detected as clicked from the button")
            if pygame.mouse.get_pressed()[0] and self.click == False:
               print("mouse was pressed and click was changed to True")
               self.click = True
            
        # if pygame.mouse.get_pressed()[0] == 0:
        #     print("mouse was changed to back to False")
        #     self.click = False
        
        