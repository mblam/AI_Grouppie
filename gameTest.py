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