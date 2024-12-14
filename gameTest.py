import pygame
import display.gameButton as b
import display.cardDisplay as c

class gameTest():
    
    def __init__(self):
        self.Check = b.gameButton(415, 705, 80, 40, "check")
        self.Call = b.gameButton(615, 705, 80, 40, "call")
        self.Raise = b.gameButton(815, 705, 80, 40, "raise")
        self.Fold = b.gameButton(1015, 705, 80, 40, "fold")
        
    def getAction(self):
        if self.Check.click == True:
            return "check"
        elif self.Call.click == True:
            return "call"
        elif self.Raise.click == True:
            return "raise"
        elif self.Fold.click == True:
            return "fold"

    def startDisplay(self, pot):
    
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
            
            #displays the buttons
            self.Check.createButton()
            self.Call.createButton()
            self.Raise.createButton()
            self.Fold.createButton()
            
            #displays the current pot of the round
            font = pygame.font.SysFont(None, 36)
            main_pot = font.render("The Pot: $" + str(pot), True, (255, 255, 255))
            screen.blit(main_pot, (1245, 363))
            
            pygame.display.flip()
        