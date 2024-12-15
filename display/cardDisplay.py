import pygame
import display.gameButton as b
CARD_WIDTH = 100

def draw_card(x,y,card_name,width=CARD_WIDTH,height=CARD_WIDTH*1.4):
    screen = pygame.display.get_surface()
    image = pygame.image.load(card_name)
    image = pygame.transform.scale(image,
                                (width,
                                    height))  # Scale it to whatever dimenstions you want
    screen.blit(image, (x, y))  # Print to the screen
    pygame.display.update()

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

#prints the players hands on the screen
def printPlayerHand(name, cards, money):
    
    #gets the current screen and text used
    screen = pygame.display.get_surface()
    text = pygame.font.SysFont(None, 24)
    
    #icon for the chip
    w_chip = pygame.transform.scale(pygame.image.load("images\chip_folder\white_chip.png"), (50,50))
    #puts the chip amount on the screen
    chip_amt = text.render(str(money), True, (255, 255, 255))
    i = 0
    y = 0
    if name == "Player 2":
        #updates the screen
        #screen.blit(p1_earnings, (25, 720))
        screen.blit(w_chip, (50, 650))
        screen.blit(chip_amt, (110, 667))
        y = 550
    else :
        #displays Player's earning so far (hard coded number for now)
        #p2_earnings = text.render("Player 2\'s Earnings: $10,000", True, (255, 255, 255))
        
        #updates the screen
        #screen.blit(p2_earnings, (25, 20))
        screen.blit(w_chip, (50, 50))
        screen.blit(chip_amt, (110, 67))
        y = 60
    for single_card in cards:
        if i == 0:
            draw_card(640, y, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png")
        else:
            draw_card(760, y, "images/Playing_Cards/PNG-cards-1.3/" + single_card  + ".png")
        i += 1