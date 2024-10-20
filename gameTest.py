# Simple pygame program

CARD_WIDTH = 100

def draw_card(x,y,text,image_name):
    width = CARD_WIDTH
    height = CARD_WIDTH*1.4
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x,y,width,height))


    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    card_font = pygame.font.SysFont('Arial Bold', 60)
    card_val = card_font.render(text,False,(0,0,0))

    screen.blit(card_val, (x + width/2 - 30,y + height/2-card_val.get_height()/2))

    image = pygame.image.load(image_name)  # Load in image
    image = pygame.transform.scale(image,
                               (card_val.get_height() * image.get_width() / image.get_height(), card_val.get_height()))  # Scale it to whatever dimenstions you want
    screen.blit(image, (x + width/2, y + height/2 - image.get_height()/2))  # Print to the screen

# Import and initialize the pygame library
import pygame

pygame.init()


# Set up the drawing window
screen = pygame.display.set_mode([500, 500])


# Run until the user asks to quit
running = True

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 0, 100))


    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    draw_card(50,50,"J","images/Card_spade.png")
    draw_card(170, 50, "Q","images/Card_diamond.png")

    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()