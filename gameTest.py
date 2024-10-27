# Import and initialize the pygame library
import pygame
# Simple pygame program

CARD_WIDTH = 100

# Set up the drawing window
screen = pygame.display.set_mode([1500, 750])

def draw_card(x,y,text,image_name,screen,width=CARD_WIDTH,height=CARD_WIDTH*1.4):
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x,y,width,height),border_radius=7)


    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    card_font = pygame.font.SysFont('Arial Bold', int(width*.6))
    card_val = card_font.render(text,False,(0,0,0))

    screen.blit(card_val, (x + width/2 - int(width*.3),y + height/2-card_val.get_height()/2))

    image = pygame.image.load(image_name)  # Load in image
    image = pygame.transform.scale(image,
                               (card_val.get_height() * image.get_width() / image.get_height(), card_val.get_height()))  # Scale it to whatever dimenstions you want
    screen.blit(image, (x + width/2, y + height/2 - image.get_height()/2))  # Print to the screen

def draw_card_upside_down(x,y,width=CARD_WIDTH,height=CARD_WIDTH*1.4):
    image = pygame.image.load("images/Card_back.png")
    image = pygame.transform.scale(image,
                                   (width,
                                    height))  # Scale it to whatever dimenstions you want
    screen.blit(image, (x, y))  # Print to the screen

def startDisplay():
    
    # Set up the drawing window
    screen = pygame.display.set_mode([1500, 750])
    
    # Fill the background with green
    screen.fill((53, 101, 73))
    
    # give a brown border
    pygame.draw.rect(screen, (111, 78, 55), (0,0,1500,750), 50)
    
    #horizontoal card to the left side 
    hori_image = pygame.image.load("images/Card_back.png")
    hori_image = pygame.transform.scale(hori_image, (100, 140))
    hori_image = pygame.transform.rotate(hori_image, 90)
    screen.blit(hori_image, (150, 325))
    
    pygame.display.flip()
    
def firstRoundBoard():
    
    draw_card(580, 305, "Q", "images/Playing_Cards/PNG-cards-1.3/2_of_spades") #First card table position
    draw_card(700, 305, "8", "images/Card_spade.png") #Second card table position
    draw_card(820, 305, "5", "images/Card_spade.png") #Third card table position