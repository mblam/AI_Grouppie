import pygame
import display.gameButton as b
import display.cardDisplay as c

class gameTest():
    
    def __init__(self):
        self.startDisplay()
        Check = False
        Call = False
        Raise = False
        Fold = False

    def startDisplay(self):
        
        screen = pygame.display.get_surface()
        
        if pygame.display.get_init():
        
            # Fill the background with green
            screen.fill((53, 101, 73))
            
            # give a brown border
            pygame.draw.rect(screen, (111, 78, 55), (0,0,1500,750), 50)
            
            #horizontoal card to the left side 
            hori_image = pygame.image.load("images/Card_back.png")
            hori_image = pygame.transform.scale(hori_image, (100, 140))
            hori_image = pygame.transform.rotate(hori_image, 90)
            screen.blit(hori_image, (150, 325))
            
            #place all of the cards in the center but with the back
            c.draw_card(460, 305, "images/Card_back.png")
            c.draw_card(580, 305, "images/Card_back.png")
            c.draw_card(700, 305, "images/Card_back.png")
            c.draw_card(820, 305, "images/Card_back.png")
            c.draw_card(940, 305, "images/Card_back.png")
            
            b.gameButton(415, 705, 80, 40, "check").createButton()
            b.gameButton(615, 705, 80, 40, "call").createButton()
            b.gameButton(815, 705, 80, 40, "raise").createButton()
            b.gameButton(1015, 705, 80, 40, "fold").createButton()
            
            pygame.display.flip()