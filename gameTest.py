# Simple pygame program

CARD_WIDTH = 100

def draw_card(x,y,text,image_name,width=CARD_WIDTH,height=CARD_WIDTH*1.4):
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

# Import and initialize the pygame library
import pygame

pygame.init()


# Set up the drawing window
screen = pygame.display.set_mode([1500, 750])


# Run until the user asks to quit
running = True

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with green
    screen.fill((53, 101, 73))


    # # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # give a brown border
    pygame.draw.rect(screen, (111, 78, 55), (0,0,1500,750), 50)

    # REMOVE LATER: line to indicate middle of screen
    # pygame.draw.line(screen, (0,0,0), (750,0), (750, 1000))
    # pygame.draw.line(screen, (0,0,0), (0,375), (1500,375))

    draw_card_upside_down(640,60) #AI first card position
    draw_card_upside_down(760, 60) #AI second card position
    draw_card(640, 550, "K", "images/Card_heart.png") #Player first card position
    draw_card(760, 550, "A", "images/Card_club.png") #Player second card position
    
    # First Round 
    # draw_card(580, 305, "Q", "images/Card_spade.png") #First card table position
    # draw_card(700, 305, "8", "images/Card_spade.png") #Second card table position
    # draw_card(820, 305, "5", "images/Card_spade.png") #Third card table position
    
    # Second Round
    # draw_card(460, 305, "Q", "images/Card_spade.png") #First card table position
    # draw_card(580, 305, "8", "images/Card_spade.png") #Second card table position
    # draw_card(700, 305, "5", "images/Card_spade.png") #Third card table position
    # draw_card_upside_down(820, 305) #Fourth card table position
    
    # Full Position
    draw_card(460, 305, "Q", "images/Card_spade.png") #First card table position
    draw_card(580, 305, "8", "images/Card_spade.png") #Second card table position
    draw_card(700, 305, "5", "images/Card_spade.png") #Third card table position
    draw_card_upside_down(820, 305) #Fourth card table position
    draw_card_upside_down(940, 305) #Fifth card table position

    hori_image = pygame.image.load("images/Card_back.png")
    hori_image = pygame.transform.scale(hori_image, (100, 140))
    hori_image = pygame.transform.rotate(hori_image, 90)
    screen.blit(hori_image, (150, 325))

    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()