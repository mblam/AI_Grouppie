import pygame

CARD_WIDTH = 100

#hex colors used
black = (0, 0, 0)
gray = (128, 128, 128)
light_gray = (192, 192, 192)

def draw_card(x,y,card_name,width=CARD_WIDTH,height=CARD_WIDTH*1.4):
    screen = pygame.display.get_surface()
    image = pygame.image.load(card_name)
    image = pygame.transform.scale(image,
                                   (width,
                                    height))  # Scale it to whatever dimenstions you want
    screen.blit(image, (x, y))  # Print to the screen
    pygame.display.update()

def startDisplay():
    
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
        draw_card(460, 305, "images/Card_back.png")
        draw_card(580, 305, "images/Card_back.png")
        draw_card(700, 305, "images/Card_back.png")
        draw_card(820, 305, "images/Card_back.png")
        draw_card(940, 305, "images/Card_back.png")
        
        pygame.display.flip()
        
        gameButton(415, 705, 80, 40, "check").createButton()
        gameButton(615, 705, 80, 40, "call").createButton()
        gameButton(815, 705, 80, 40, "raise").createButton()
        gameButton(1015, 705, 80, 40, "fold").createButton()

#prints for the first round    
def firstRoundBoard(cards):
    print("prints the cards for the first round")
    print(cards)
    i = 0
    for single_card in cards:
        if i == 0:
            draw_card(580, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #First card table position
        elif i == 1:    
            draw_card(700, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #Second card table position
        else: 
            draw_card(820, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #Third card table position  
        i += 1

#prints for the first round    
def secondRoundBoard(cards):
    print("prints the cards for the first round")
    print(cards)
    i = 0
    for single_card in cards:
        if i == 0:
            draw_card(460, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #First card table position
        elif i == 1:    
            draw_card(580, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #Second card table position
        elif i == 2: 
            draw_card(700, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #Third card table position
        else:
            draw_card(820, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #Third card table position
        i += 1

def thirdRoundBoard(cards):
    print("prints the cards for the first round")
    print(cards)
    i = 0
    for single_card in cards:
        if i == 0:
            draw_card(460, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #First card table position
        elif i == 1:    
            draw_card(580, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #Second card table position
        elif i == 2: 
            draw_card(700, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #Third card table position
        elif i == 3: 
            draw_card(820, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #Third card table position
        else:
            draw_card(940, 305, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png") #Third card table position
        i += 1

#prints the players hands
def printPlayerHand(name, cards):
    print(name)
    print(cards)
    i = 0
    y = 0
    if name == "Player 1":
        y = 550
    else :
        y = 60
    for single_card in cards:
        if i == 0:
            draw_card(640, y, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png")
        else:
            draw_card(760, y, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png")
        i += 1
        
class gameButton():

    def __init__(self, x_pos, y_pos, width, height, title):
        self.x_pos = x_pos
        self.y_pos= y_pos
        self.title = title
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.surface = pygame.Surface((width, height))
        self.click = False
    
    def createButton(self):
        font = pygame.font.SysFont(None, 24)
        #gets the font
        text = font.render(self.title, True, gray)
        
        #gets the coordinates for the text
        button_text = text.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))
        
        #creates the button
        pygame.draw.rect(self.surface, gray, self.rect)
        
        #display text on button surface
        self.surface.blit(text, button_text)
        
        #displays the acatual button
        pygame.display.get_surface().blit(self.surface, (self.x_pos, self.y_pos))