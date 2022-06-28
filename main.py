import pygame, sys
from  game import create_screen, gameplay, gameControls

screen = create_screen()

# Load images
background_surf = pygame.image.load("assets/background3.jpg")

# scale images
background_surf = pygame.transform.scale(background_surf, (500, 1200))

# initial y position of background
background_pos_y = -600


while True:
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()

        gameControls(event)

    screen.blit(background_surf, (0, background_pos_y))

    gameplay()

    # moving the background
    background_pos_y+=1
    # resetting the background to -500
    if(background_pos_y == 0):
        background_pos_y = -500




    pygame.display.update()
