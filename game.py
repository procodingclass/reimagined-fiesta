import pygame, random, sys
import ctypes

screen_width = 500
screen_height = 600

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width,screen_height))

def create_screen():
    global screen
    return screen


def loadImages(images_path):
    image_list = []

    for path in images_path:
        loaded_image = pygame.image.load(path).convert_alpha()
        image_list.append(loaded_image)
    return image_list

def scaleImages(image_list, width, height):
    scaled_images = []
    if(len(image_list) == 1):
        return pygame.transform.scale(image_list[0], (width, height))

    for img in image_list:
        image = pygame.transform.scale(img, (width, height))
        scaled_images.append(image)

    return scaled_images


def flipImages(image_list):
    fliped_images = []
    if(len(image_list) == 1):
        return pygame.transform.flip(image_list[0],True,False)

    for img in image_list:
        image = pygame.transform.flip(img,True,False)
        fliped_images.append(image)

    return fliped_images


def check_collision(static_rect, moving_rect, vel_x, vel_y):
    # x- direction
    moving_rect_props = (moving_rect.x + vel_x, moving_rect.y, moving_rect.width, moving_rect.height)
    if static_rect.colliderect(moving_rect_props):
            vel_x = 0

            #check for collision in y direction
            moving_rect_props = (moving_rect.x, moving_rect.y + vel_y, moving_rect.width, moving_rect.height)
            if static_rect.colliderect(moving_rect_props):
                #check if below the platform i.e. jumping
                if(vel_y < 0):
                    vel_y = static_rect.bottom - moving_rect.top
                elif(vel_y > 0): #check if above the platform i.e. falling
                    vel_y = static_rect.top - moving_rect.bottom

    # make player to stand on platform
    # y- direction
    static_rect_props = (static_rect.x, static_rect.y - vel_y, static_rect.width, static_rect.height)
    if(moving_rect.colliderect(static_rect_props)):
        vel_y = 0
    return vel_x, vel_y


# --------- Jumping Joe -----------
platforms = []
coin_animation_counter = 0
player_animation_counter  = 0
enemy_animation_counter = 0
player_vel_x = 0
player_vel_y = 0
score = 0
collected_coins = 0

enemy_vel_x = 1


platform_surf =loadImages(["assets/platform.png"])
stone_surf = loadImages(["assets/stone.png"])
flower_surf = loadImages(["assets/flower1.png"])
bush_surf = loadImages(["assets/bush.png"])
coin_surf = loadImages([
    "assets/coin/1.png","assets/coin/2.png","assets/coin/3.png",
    "assets/coin/4.png","assets/coin/5.png","assets/coin/6.png",
    "assets/coin/7.png","assets/coin/8.png","assets/coin/9.png",
    "assets/coin/10.png","assets/coin/11.png","assets/coin/12.png",
    "assets/coin/13.png","assets/coin/14.png","assets/coin/15.png",
    "assets/coin/16.png"])

player_right_surf = loadImages(["assets/joe/0.png","assets/joe/1.png",
    "assets/joe/2.png","assets/joe/3.png","assets/joe/4.png"])

bird_right_surf = loadImages(["assets/bird/1.png","assets/bird/2.png",
    "assets/bird/3.png","assets/bird/4.png"])

egg_surf = loadImages(["assets/egg.png"])
energy_ball_surf = loadImages(["assets/energyball.png"])
ufo_surf = loadImages(["assets/ufo.png"])



# scale images
coin_surf = scaleImages(coin_surf, 30, 30)
player_right_surf = scaleImages(player_right_surf, 30, 43)
bird_right_surf = scaleImages(bird_right_surf, 40, 40)

# flip images
player_left_surf = flipImages(player_right_surf)
bird_left_surf = flipImages(bird_right_surf)

# create player surface
player_surf = player_right_surf

# create enemy surface
enemy_surf = bird_right_surf

# create object rectangle
player_rect =pygame.Rect(200,120,30,43)
player_rect.center =(250,300)

enemy_rect = pygame.Rect(10, 10, 40, 40)
egg_rect = pygame.Rect(10,10,egg_surf[0].get_width(),egg_surf[0].get_height())






score_font = pygame.font.Font('freesansbold.ttf', 16)
over_font = pygame.font.Font('freesansbold.ttf', 25)

def createPlatform(x,y):
    global platforms

    platforms.append({
        "rect" : pygame.Rect(x,y,70,15),
        "type" : random.choice(["stone", "flower", "bush", "coin"])
        })

def handleGameControls():
    global player_surf, player_right_surf, player_left_surf
    global player_vel_x, player_vel_y, player_animation_counter

    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()

        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_LEFT):
                player_animation_counter += 1
                player_surf = player_left_surf
                player_vel_x = -5

            if(event.key == pygame.K_RIGHT):
                player_animation_counter+=1
                player_surf = player_right_surf
                player_vel_x = 5

            if(event.key == pygame.K_UP):
                player_vel_y = -18
                player_animation_counter = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_vel_x = 0
            if event.key == pygame.K_RIGHT:
                player_vel_x = 0
            # if event.key == pygame.K_SPACE:
            #     gameState="play"
            # if event.key == pygame.K_r and gameState=="end":
            #     player.center=[250,300]
            #     score=0
            #     gameState="play"
            #     collected_coins=0
            #     bg_index=0
            #     bird_animation_right=loadAnimations(["assets/bird/1.png","assets/bird/2.png","assets/bird/3.png","assets/bird/4.png"])
            #     bird_animation_left=flipAnimations(bird_animation_right)
            #     egg_surf=pygame.image.load("assets/bird/egg.png")
            #     enemy_animation=bird_animation_right
            #     platforms[5][0].x=220
            #     platforms[5][0].y=350
            #     enemy.x=-99
            #     enemy_velocity=-3



def initialPlatforms():
    createPlatform(80,-60)
    createPlatform(200,0)
    createPlatform(100,60)
    createPlatform(420,120)
    createPlatform(100,180)
    createPlatform(200,240)
    createPlatform(340,300)
    createPlatform(200,360)
    createPlatform(10,420)
    createPlatform(400,480)
    createPlatform(420,540)

initialPlatforms()


def gameplay():
    global platforms, stone_surf, screen, coin_animation_counter
    global player_rect, player_surf, player_animation_counter
    global player_vel_x, player_vel_y, screen_height, score
    global screen_width, screen_height, collected_coins
    global enemy_animation_counter, enemy_surf, enemy_rect, egg_rect
    global enemy_vel_x, egg_surf, ufo_surf, energy_ball_surf

    try:
        from main import game_state


        if(coin_animation_counter >= len(coin_surf)):
            coin_animation_counter = 0

        if(player_animation_counter >= len(player_surf)):
            player_animation_counter = 0

        if(enemy_animation_counter >= len(enemy_surf)):
            enemy_animation_counter = 0

        for platform in platforms:
            screen.blit(platform_surf[0],platform["rect"])

            if(game_state == "play"):
                platform["rect"].y+= (2+int(score/400))

            if(platform["type"] == "flower"):
                screen.blit(flower_surf[0],(platform["rect"].x,platform["rect"].y - 25))
            elif(platform["type"] == "stone"):
                screen.blit(stone_surf[0],(platform["rect"].x,platform["rect"].y - 20))
            elif(platform["type"] == "bush"):
                screen.blit(bush_surf[0],(platform["rect"].x,platform["rect"].y - 25))
            elif(platform["type"] == "coin"):
                screen.blit(coin_surf[coin_animation_counter],(platform["rect"].x+20,platform["rect"].y-35))

                # collision between player and coin
                if player_rect.colliderect(platform["rect"].x+20,platform["rect"].y-25,coin_surf[coin_animation_counter].get_width(),coin_surf[coin_animation_counter].get_height()):
                    platform["type"]= ""
                    collected_coins += 1
                    score+=10


            if(platform["rect"].y > (screen_height + 130)):
                platforms.remove(platform)
                createPlatform(random.randint(0,420),-40)

            #check collision with platform if moved by player_vel_y
            if player_rect.colliderect(platform["rect"].x,platform["rect"].y - player_vel_y,
                platform["rect"].width,platform["rect"].height) and player_rect.y < platform["rect"].y and player_vel_y>0:
                        player_vel_y = 0

        coin_animation_counter+=1

        screen.blit(player_surf[player_animation_counter], player_rect)

        if game_state=="initial":
            player_rect.center=(250,300)
            score=0
        elif(game_state == "play"):

            # handle game controls
            handleGameControls()

            # Adding gravity
            player_vel_y += 0.8

            if(player_vel_x != 0):
                player_animation_counter = 0

            #Calculating the score and increasing it only when player goes up
            if(player_vel_y < 0):
                score+=1


            # bring back the player to the canvas
            if(player_rect.x < -30):
                player_rect.x = screen_width

            if (player_rect.x > screen_width):
                player_rect.x = -30

            # update player x and y in each frame
            player_rect.x += player_vel_x
            player_rect.y += player_vel_y

            # update enemy x in each frame
            enemy_rect.x += enemy_vel_x
            # egg_rect.y += 2


            if enemy_rect.x > (screen_width + 100):
               enemy_surf = bird_left_surf
               enemy_vel_x *= -1
            elif enemy_rect.x < -100:
               enemy_surf = bird_right_surf
               enemy_vel_x *= -1


            if score >  250:
                enemy_surf = ufo_surf
                if enemy_surf == ufo_surf:
                    egg_surf = energy_ball_surf

            screen.blit(egg_surf[0],egg_rect)
            screen.blit(enemy_surf[enemy_animation_counter],enemy_rect)

            enemy_animation_counter += 1

        elif game_state=="end":
            score_text = over_font.render(str(score), False, (255,255,255))
            screen.blit(score_text,(240,250))

        # show score count
        score_text = score_font.render("Score : "+ str(score), False, (3,3,3))
        screen.blit(score_text,(10,10))

        # show coins count
        coin_text = score_font.render("X"+ str(collected_coins), False, (3,3,3))
        screen.blit(coin_text,(465,18))
        screen.blit(coin_surf[0],(430,10))

    except:
        pass

    clock.tick(30)
