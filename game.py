import pygame
import pygame.freetype
from random import random, randrange as rnd
import os

#Game window configuration
width = 1024
height = 768
fps = 60

#Setup game
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Breakout")
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.freetype.SysFont('Segoe UI Variable', 18)
font2 = pygame.font.SysFont('Segoe UI Variable', 18)
titlefont = pygame.font.SysFont('Segoe UI Variable', 60)
highscore = "highscore.txt"
icon = pygame.image.load("assets/icon/icon.png").convert_alpha()
pygame.display.set_icon(icon)
logo = pygame.image.load("assets/logo/logo.png").convert_alpha()
logo = pygame.transform.scale(logo, (500, 200))

#Sound effects
ball_hit_sfx = pygame.mixer.Sound("assets/sounds/BallHit.wav")
game_over_lose_all_lives_sfx = pygame.mixer.Sound("assets/sounds/GameOverLoseAllLives.wav")
newrecord_sfx = pygame.mixer.Sound("assets/sounds/newrecord.wav")
level_complete_sfx = pygame.mixer.Sound("assets/sounds/tada.wav")
lose_a_life_sfx = pygame.mixer.Sound("assets/sounds/LoseALife.wav")
brick_break_sfx = pygame.mixer.Sound("assets/sounds/BrickBreak.wav")
complete_10_levels_sfx = pygame.mixer.Sound("assets/sounds/completed10levels.wav")
extra_life_sfx = pygame.mixer.Sound("assets/sounds/1up.wav")

#Volumes
sfx_volume = 0.4
song_volume = 0.7

ball_hit_sfx.set_volume(sfx_volume)
game_over_lose_all_lives_sfx.set_volume(sfx_volume)
newrecord_sfx.set_volume(sfx_volume)
level_complete_sfx.set_volume(sfx_volume)
lose_a_life_sfx.set_volume(sfx_volume)
brick_break_sfx.set_volume(sfx_volume)

#Songs
songnumber = 0
song = pygame.mixer.music.load(f"assets/music/{str(songnumber)}.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(song_volume)

#Background image
imgnumber = 0
img = pygame.image.load(f'assets/backgrounds/{str(imgnumber)}.jpg').convert()
img = pygame.transform.scale(img, (width, height))

#Help images
helpimg = pygame.image.load("assets/help/mainhelp.jpg").convert()
helpimg = pygame.transform.scale(helpimg, (500, 500))

#Collision detection
def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top
    
    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

#Button settings
def button(sc, position, text):
    buttonfont = pygame.font.SysFont("Segoe UI Variable", 30)
    text_render = buttonfont.render(text, 1, (0, 0, 0))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.rect(sc, (255, 255, 255), (x, y, w, h))
    return sc.blit(text_render, (x, y))

#Draw game event
def draw_game():
    [pygame.draw.rect(sc, color_list[color], brick) for color, brick in enumerate(brick_list)]
    pygame.draw.rect(sc, pygame.Color(paddle_colors[paddle_colors_index_number]), paddle)
    pygame.draw.circle(sc, pygame.Color('black'), ball.center, ball_radius, 7, True, True, True, True)
    pygame.draw.circle(sc, pygame.Color(ball_colors[ball_colors_index_number]), ball.center, ball_radius)

#Draw level complete message
def level_complete_message():
    rendersuccesstext = titlefont.render("Level Complete!", True, (255, 255, 255))
    sc.blit(rendersuccesstext, (300, 100))
    if level == 10:
        rendertenlevelsawardtext = font2.render("You explored 10 places, what a great adventure!", True, (255, 255, 255))
        sc.blit(rendertenlevelsawardtext, (300, 300))
        rendertenlevelsawardtextpart2 = font2.render("But it isn't end yet! After that, let's keep revisiting all of them!", True, (255, 255, 255))
        sc.blit(rendertenlevelsawardtextpart2, (300, 350))
    renderadvancetext = titlefont.render(f"Next to Level {level+1}", True, (255, 255, 255))
    sc.blit(renderadvancetext, (300, 500))

    pygame.display.update()

    while True:
        pygame.time.delay(5000)
        break

def get_highscore():
    if os.path.exists(highscore):
        with open(highscore, "r") as f:
            return f.read()
    else:
        with open(highscore, "w") as f:
            f.write(str(score))

#Paddle settings
paddle_w = 150
paddle_h = 35
paddle_speed = 24
paddle = pygame.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)
paddle_colors = ['orange', [158, 158, 158], 'white', 'black', 'blue', [0, 23, 128], 'red', 'yellow', 'green', 'pink', 'purple', 'brown']
paddle_colors_index_number = 0
paddle_colors_index = "Orange"

#Ball settings
ball_radius = 20
ball_speed = 7
ball_rect = int(ball_radius * 2 ** 0.5)
ball_colors = [[158, 158, 158], 'white', 'black', 'blue', [0, 23, 128], 'red', 'yellow', 'green', 'pink', 'purple', 'brown', 'orange']
ball_colors_index_number = 0
ball_colors_index = "Grey"
ball = pygame.Rect(paddle.x + (paddle_w // 2), paddle.y - paddle_h, ball_rect, ball_rect)
dx = 1
dy = -1

#Brick settings
bricky = 80
brickx = 40
bricknumberj = 4
brick_list = [pygame.Rect(brickx + 125 * i, bricky + 40 * j, 80, 30) for i in range(8) for j in range(bricknumberj)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(8) for j in range(bricknumberj)]

#Variables
pause = 0
lives = 4
level = 1
score = 0
lifescore = 0
songvolumecounter = 7
soundvolumecounter = 4
gamestart = False
isgameplayed = False
show_menu = True
level_complete = False
game_over = False
give_up_decision = False
erase_highscore_decision = False
show_options_menu = False
show_help_menu = False
highscorenum = 0
tophighscore = get_highscore()
extra = 0

#Options Menu Buttons variables
reducesoundvolumebutton = button(sc, (300, 250), "-")
increasesoundvolumebutton = button(sc, (400, 250), "+")
reducesongvolumebutton = button(sc, (300, 340), "-")
increasesongvolumebutton = button(sc, (400, 340), "+")
erasehighscorebutton = button(sc, (300, 450), "Erase Highscore")
backtomainbutton = button(sc, (300, 540), "Back to Main")
previousspherecolorbutton = button(sc, (300, 450), "<")
nextspherecolorbutton = button(sc, (400, 450), ">")
previouspaddlecolorbutton = button(sc, (300, 510), "<")
nextpaddlecolorbutton = button(sc, (480, 510), ">")

eraseconfirmbutton = button(sc, (260, 230), "Yes")
erasenobutton = button(sc, (340, 230), "No")

#Help variables (including buttons)
helpindex = 1
helpindexsection = "Introduction"
helpbacktomainbutton = button(sc, (100, 580), "Back to Main")
helppreviousbutton = button(sc, (580, 660), "Previous")
helpnextbutton = button(sc, (850, 660), "Next")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over == True:
                if retrybutton.collidepoint(pygame.mouse.get_pos()):
                    if isgameplayed == True:
                        game_over = False
                        game_over_lose_all_lives_sfx.stop()
                        newrecord_sfx.stop()
                        tophighscore = int(get_highscore())
                        imgnumber = 1
                        img = pygame.image.load(f'assets/backgrounds/{str(imgnumber)}.jpg').convert()
                        img = pygame.transform.scale(img, (width, height))
                        sc.blit(img, (0, 0))
                        score = 0
                        lives = 4
                        score = 0
                        level = 1
                        lifescore = 0
                        pause = 0
                        ball_speed = 7
                        bricknumberj = 4
                        paddle = pygame.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)
                        ball = pygame.Rect(paddle.x + (paddle_w // 2), paddle.y - paddle_h, ball_rect, ball_rect)
                        brick_list = [pygame.Rect(brickx + 125 * i, bricky + 40 * j, 80, 30) for i in range(8) for j in range(bricknumberj)]
                        color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(8) for j in range(bricknumberj)]
                        give_up_decision = False
                        gamestart = False
                        songnumber = 1
                        song = pygame.mixer.music.load(f"assets/music/{str(songnumber)}.mp3")
                        pygame.mixer.music.play(-1)
                elif backtomainscreenbutton.collidepoint(pygame.mouse.get_pos()):
                    if isgameplayed == True:
                        game_over = False
                        game_over_lose_all_lives_sfx.stop()
                        newrecord_sfx.stop()
                        tophighscore = int(get_highscore())
                        imgnumber = 0
                        img = pygame.image.load(f'assets/backgrounds/{str(imgnumber)}.jpg').convert()
                        img = pygame.transform.scale(img, (width, height))
                        sc.blit(img, (0, 0))
                        score = 0
                        lives = 4
                        score = 0
                        level = 1
                        lifescore = 0
                        pause = 0
                        ball_speed = 7
                        bricknumberj = 4
                        paddle = pygame.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)
                        ball = pygame.Rect(paddle.x + (paddle_w // 2), paddle.y - paddle_h, ball_rect, ball_rect)
                        brick_list = [pygame.Rect(brickx + 125 * i, bricky + 40 * j, 80, 30) for i in range(8) for j in range(bricknumberj)]
                        color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(8) for j in range(bricknumberj)]
                        give_up_decision = False
                        show_menu = True
                        isgameplayed = False
                        songnumber = 0
                        song = pygame.mixer.music.load(f"assets/music/{str(songnumber)}.mp3")
                        pygame.mixer.music.play(-1)
            if give_up_decision == True:
                if confirmbutton.collidepoint(pygame.mouse.get_pos()):
                    if isgameplayed == True:
                        pygame.mixer.music.stop()
                        game_over = True
                        gamestart = False
                        if score < tophighscore and level < 256:
                            game_over_lose_all_lives_sfx.play()
                        if score > tophighscore or level >= 256:
                            newrecord_sfx.play()
                elif nobutton.collidepoint(pygame.mouse.get_pos()):
                    if isgameplayed == True:
                        give_up_decision = False
            if show_menu == True:
                if playbutton.collidepoint(pygame.mouse.get_pos()):
                    imgnumber = 1
                    img = pygame.image.load(f'assets/backgrounds/{str(imgnumber)}.jpg').convert()
                    img = pygame.transform.scale(img, (width, height))
                    sc.blit(img, (0, 0))
                    songnumber = 1
                    pygame.mixer.music.stop()
                    song = pygame.mixer.music.load(f"assets/music/{str(songnumber)}.mp3")
                    pygame.mixer.music.play(-1)
                    show_menu = False
                    isgameplayed = True
                elif optionsbutton.collidepoint(pygame.mouse.get_pos()):
                    show_options_menu = True
                    show_menu = False
                elif helpbutton.collidepoint(pygame.mouse.get_pos()):
                    show_help_menu = True
                    show_menu = False
                elif exitbutton.collidepoint(pygame.mouse.get_pos()):
                    exit()
            if pause == 1:
                if reducesoundvolumebutton.collidepoint(pygame.mouse.get_pos()):
                    if soundvolumecounter > 0:
                        sfx_volume -= 0.1
                        ball_hit_sfx.set_volume(sfx_volume)
                        game_over_lose_all_lives_sfx.set_volume(sfx_volume)
                        newrecord_sfx.set_volume(sfx_volume)
                        level_complete_sfx.set_volume(sfx_volume)
                        lose_a_life_sfx.set_volume(sfx_volume)
                        brick_break_sfx.set_volume(sfx_volume)
                        soundvolumecounter -= 1
                elif increasesoundvolumebutton.collidepoint(pygame.mouse.get_pos()):
                    if soundvolumecounter < 10:
                        sfx_volume += 0.1
                        ball_hit_sfx.set_volume(sfx_volume)
                        game_over_lose_all_lives_sfx.set_volume(sfx_volume)
                        newrecord_sfx.set_volume(sfx_volume)
                        level_complete_sfx.set_volume(sfx_volume)
                        lose_a_life_sfx.set_volume(sfx_volume)
                        brick_break_sfx.set_volume(sfx_volume)
                        soundvolumecounter += 1
                elif reducesongvolumebutton.collidepoint(pygame.mouse.get_pos()):
                    if songvolumecounter > 0:
                        song_volume -= 0.1
                        pygame.mixer.music.set_volume(song_volume)
                        songvolumecounter -= 1
                elif increasesongvolumebutton.collidepoint(pygame.mouse.get_pos()):
                    if songvolumecounter < 10:
                        song_volume += 0.1
                        pygame.mixer.music.set_volume(song_volume)
                        songvolumecounter += 1
                elif giveupbutton.collidepoint(pygame.mouse.get_pos()):
                    give_up_decision = True
            if show_options_menu == True:
                if reducesoundvolumebutton.collidepoint(pygame.mouse.get_pos()):
                    if soundvolumecounter > 0:
                        sfx_volume -= 0.1
                        ball_hit_sfx.set_volume(sfx_volume)
                        game_over_lose_all_lives_sfx.set_volume(sfx_volume)
                        newrecord_sfx.set_volume(sfx_volume)
                        level_complete_sfx.set_volume(sfx_volume)
                        lose_a_life_sfx.set_volume(sfx_volume)
                        brick_break_sfx.set_volume(sfx_volume)
                        soundvolumecounter -= 1
                elif increasesoundvolumebutton.collidepoint(pygame.mouse.get_pos()):
                    if soundvolumecounter < 10:
                        sfx_volume += 0.1
                        ball_hit_sfx.set_volume(sfx_volume)
                        game_over_lose_all_lives_sfx.set_volume(sfx_volume)
                        newrecord_sfx.set_volume(sfx_volume)
                        level_complete_sfx.set_volume(sfx_volume)
                        lose_a_life_sfx.set_volume(sfx_volume)
                        brick_break_sfx.set_volume(sfx_volume)
                        soundvolumecounter += 1
                elif reducesongvolumebutton.collidepoint(pygame.mouse.get_pos()):
                    if songvolumecounter > 0:
                        song_volume -= 0.1
                        pygame.mixer.music.set_volume(song_volume)
                        songvolumecounter -= 1
                elif increasesongvolumebutton.collidepoint(pygame.mouse.get_pos()):
                    if songvolumecounter < 10:
                        song_volume += 0.1
                        pygame.mixer.music.set_volume(song_volume)
                        songvolumecounter += 1
                elif erasehighscorebutton.collidepoint(pygame.mouse.get_pos()):
                    if os.path.exists(highscore):
                        erase_highscore_decision = True
                elif previousspherecolorbutton.collidepoint(pygame.mouse.get_pos()):
                    if ball_colors_index_number > 0:
                        ball_colors_index_number -= 1
                elif nextspherecolorbutton.collidepoint(pygame.mouse.get_pos()):
                    if ball_colors_index_number < 11:
                        ball_colors_index_number += 1
                elif previouspaddlecolorbutton.collidepoint(pygame.mouse.get_pos()):
                    if paddle_colors_index_number > 0:
                        paddle_colors_index_number -= 1
                elif nextpaddlecolorbutton.collidepoint(pygame.mouse.get_pos()):
                    if paddle_colors_index_number < 11:
                        paddle_colors_index_number += 1
                elif backtomainbutton.collidepoint(pygame.mouse.get_pos()):
                    show_options_menu = False
                    show_menu = True
            if erase_highscore_decision == True:
                if eraseconfirmbutton.collidepoint(pygame.mouse.get_pos()):
                    os.remove(highscore)
                    lose_a_life_sfx.play()
                    erase_highscore_decision = False
                elif erasenobutton.collidepoint(pygame.mouse.get_pos()):
                    erase_highscore_decision = False
            if show_help_menu == True:
                if helpbacktomainbutton.collidepoint(pygame.mouse.get_pos()):
                    helpindex = 1
                    show_help_menu = False
                    show_menu = True
                elif helppreviousbutton.collidepoint(pygame.mouse.get_pos()):
                    if helpindex > 1:
                        helpindex -= 1
                elif helpnextbutton.collidepoint(pygame.mouse.get_pos()):
                    if helpindex < 9:
                        helpindex += 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if isgameplayed == True:
                    if game_over == False:
                        gamestart = True
                    else:
                        gamestart = False
            if event.key == pygame.K_p:
                if isgameplayed == True:
                    if give_up_decision == False:
                        if pause == 0:
                            pause = 1
                        else:
                            pause = 0

    sc.blit(img, (0, 0))

    #Get highest score
    try:
        highscorenum = int(get_highscore())
    except:
        highscorenum = 0

    #Drawing title screen
    if show_menu:
        tophighscore = int(get_highscore())
        
        sc.blit(logo, (250, 150))
        renderhighscorenumbertext = font2.render(f"Highest Score: {highscorenum}", True, (255, 255, 255))
        sc.blit(renderhighscorenumbertext, (700, 720))
        playbutton = button(sc, (480, 400), "Play")
        helpbutton = button(sc, (480, 480), "Help")
        optionsbutton = button(sc, (480, 560), "Options")
        exitbutton = button(sc, (480, 640), "Exit")

    if isgameplayed == True:
        #Drawing main game
        statusborder = pygame.draw.rect(sc, (0, 0, 0), (0, 0, width, 60))
        livestextrender = font.render_to(sc, (statusborder.x + 20, statusborder.y + 25), f"Lives: {str(lives)}", (255, 255, 255))
        scoretextrender = font.render_to(sc, (livestextrender.x + 240, statusborder.y + 25), f"Score: {str(score)}", (255, 255, 255))
        highscoretextrender = font.render_to(sc, (livestextrender.x + 480, statusborder.y + 25), f"Highest Score: {str(highscorenum)}", (255, 255, 255))
        leveltextrender = font.render_to(sc, (scoretextrender.x + 550, statusborder.y + 25), f"Level: {str(level)}", (255, 255, 255))
        draw_game()

        if gamestart == True:
            if pause < 1:
                #Ball movement
                ball.x += ball_speed * dx
                ball.y += ball_speed * dy

                #Ball collision left/right
                if ball.centerx < ball_radius or ball.centerx > width - ball_radius:
                    dx = -dx
                    ball_hit_sfx.play()
    
                #Ball collision top
                if ball.centery < ball_radius:
                    dy = -dy
                    ball_hit_sfx.play()
    
                #Ball collision paddle
                if ball.colliderect(paddle) and dy > 0:
                    dx, dy = detect_collision(dx, dy, ball, paddle)
                    ball_hit_sfx.play()
            
                #Ball collision border
                if ball.colliderect(statusborder) and dy < 0:
                    dx, dy = detect_collision(dx, dy, ball, statusborder)
                    ball_hit_sfx.play()
            
                #Ball collision bricks
                hit_index = ball.collidelist(brick_list)
                if hit_index != -1:
                    hit_rect = brick_list.pop(hit_index)
                    hit_color = color_list.pop(hit_index)
                    dx, dy = detect_collision(dx, dy, ball, hit_rect)
                    brick_break_sfx.play()
                    score += 1000
                    lifescore += 1001
            
                #Lose a life
                if ball.bottom > height:
                    lives -= 1
                    lose_a_life_sfx.play()
                    if game_over == False:
                        ball = pygame.Rect(paddle.x + (paddle_w // 2), paddle.y - paddle_h, ball_rect, ball_rect)
                    
                    gamestart = False
            
                #TODO: Gain a extra life if score reaches to every 100000 points
                if lives < 100:
                    if score % 100000 == 0:
                        if lifescore / 100100:
                            lives += 1
                            lifescore -= lifescore
                            extra_life_sfx.play()
            
                #Game over
                if lives <= 0 or level > 255:
                    pygame.mixer.music.stop()
                    game_over = True
                    gamestart = False
                    if score < tophighscore and level < 256:
                        game_over_lose_all_lives_sfx.play()
                    if score > tophighscore or level >= 256:
                        newrecord_sfx.play()
            
                #Next level
                if not len(brick_list):
                    level_complete = True
                    pygame.mixer.music.stop()
                    if level == 10:
                        complete_10_levels_sfx.play()
                    else:
                        level_complete_sfx.play()
                    if level_complete:
                        level_complete_message()
                    
                    level_complete = False
                    if imgnumber < 10 and songnumber < 10:
                        imgnumber += 1
                        songnumber += 1
                    else:
                        imgnumber = 1
                        songnumber = 1
                    if level > 2 and level < 5:
                        ball_speed = 8
                        bricknumberj = 5
                    if level > 5 and level < 10:
                        ball_speed = 10
                        bricknumberj = 6
                    if level > 10:
                        ball_speed = 12
                        bricknumberj = 7
                    song = pygame.mixer.music.load(f"assets/music/{str(songnumber)}.mp3")
                    img = pygame.image.load(f'assets/backgrounds/{str(imgnumber)}.jpg').convert()
                    img = pygame.transform.scale(img, (width, height))
                    sc.blit(img, (0, 0))
                    paddle = pygame.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)
                    ball = pygame.Rect(paddle.x + (paddle_w // 2), paddle.y - paddle_h, ball_rect, ball_rect)
                    level += 1
                    brick_list = [pygame.Rect(brickx + 125 * i, bricky + 40 * j, 80, 30) for i in range(8) for j in range(bricknumberj)]
                    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(8) for j in range(bricknumberj)]
                    gamestart = False
                    pygame.mixer.music.play(-1)
                
                #Checking highest score
                if(highscorenum < score):
                    highscorenum = score
                with open(highscore, "w") as f:
                    f.write(str(highscorenum))

                #Control paddle
                key = pygame.key.get_pressed()
                if key[pygame.K_LEFT] and paddle.left > 0:
                    paddle.left -= paddle_speed
                if key[pygame.K_RIGHT] and paddle.right < width:
                    paddle.right += paddle_speed
            else:
                if give_up_decision == False:
                    renderpausetext = titlefont.render("Paused!", True, (255, 255, 255))
                    sc.blit(renderpausetext, (300, 100))
                    rendersoundvolumetext = font2.render("Sound Volume", True, (255, 255, 255))
                    sc.blit(rendersoundvolumetext, (300, 210))
                    rendersoundvolumenumbertext = font2.render(str(soundvolumecounter), True, (255, 255, 255))
                    sc.blit(rendersoundvolumenumbertext, (350, 260))
                    reducesoundvolumebutton = button(sc, (300, 250), "-")
                    increasesoundvolumebutton = button(sc, (400, 250), "+")
                    rendersongvolumetext = font2.render("Song Volume", True, (255, 255, 255))
                    sc.blit(rendersongvolumetext, (300, 305))
                    rendersongvolumenumbertext = font2.render(str(songvolumecounter), True, (255, 255, 255))
                    sc.blit(rendersongvolumenumbertext, (350, 347))
                    reducesongvolumebutton = button(sc, (300, 340), "-")
                    increasesongvolumebutton = button(sc, (400, 340), "+")
                    giveupbutton = button(sc, (300, 430), "Give Up")
                else:
                    renderareyousuregiveuptext = font2.render("Are you sure do you want to give up?", True, (255, 255, 255))
                    sc.blit(renderareyousuregiveuptext, (260, 150))
                    confirmbutton = button(sc, (260, 230), "Yes")
                    nobutton = button(sc, (340, 230), "No")
                pygame.display.update()
        elif game_over:
            rendergameovertext = titlefont.render("Game Over", True, (255, 255, 255))
            sc.blit(rendergameovertext, (300, 100))
            if level > 255:
                rendercongratstext = font2.render("Congratulations! You're a super player!", True, (255, 255, 255))
                sc.blit(rendercongratstext, (300, 200))
                renderscoreguesstext = font2.render(f"You beated {score} points!", True, (255, 255, 255))
                sc.blit(renderscoreguesstext, (300, 250))
                if score > tophighscore:
                    rendernewrecordtext = font2.render("New record!", True, (255, 255, 255))
                    sc.blit(rendernewrecordtext, (300, 260))
                retrybutton = button(sc, (300, 320), "Retry")
                backtomainscreenbutton = button(sc, (400, 320), "Back to Main Screen")
            else:
                renderscoreguesstext = font2.render(f"You beated {score} points!", True, (255, 255, 255))
                sc.blit(renderscoreguesstext, (300, 200))
                if score > tophighscore:
                    rendernewrecordtext = font2.render("New record!", True, (255, 255, 255))
                    sc.blit(rendernewrecordtext, (300, 260))
                retrybutton = button(sc, (300, 320), "Retry")
                backtomainscreenbutton = button(sc, (400, 320), "Back to Main Screen")
            
            pygame.display.update()
    elif show_options_menu == True:
        if erase_highscore_decision == False:
            reducesoundvolumebutton = button(sc, (300, 180), "-")
            increasesoundvolumebutton = button(sc, (400, 180), "+")
            reducesongvolumebutton = button(sc, (300, 270), "-")
            increasesongvolumebutton = button(sc, (400, 270), "+")
            previousspherecolorbutton = button(sc, (300, 360), "<")
            nextspherecolorbutton = button(sc, (480, 360), ">")
            previouspaddlecolorbutton = button(sc, (300, 440), "<")
            nextpaddlecolorbutton = button(sc, (480, 440), ">")

            ball_colors_index = "Grey"
            paddle_colors_index = "Orange"

            if ball_colors_index_number == 0:
                ball_colors_index = "Grey"
            elif ball_colors_index_number == 1:
                ball_colors_index = "White"
            elif ball_colors_index_number == 2:
                ball_colors_index = "Black"
            elif ball_colors_index_number == 3:
                ball_colors_index = "Blue"
            elif ball_colors_index_number == 4:
                ball_colors_index = "Dark Blue"
            elif ball_colors_index_number == 5:
                ball_colors_index = "Red"
            elif ball_colors_index_number == 6:
                ball_colors_index = "Yellow"
            elif ball_colors_index_number == 7:
                ball_colors_index = "Green"
            elif ball_colors_index_number == 8:
                ball_colors_index = "Pink"
            elif ball_colors_index_number == 9:
                ball_colors_index = "Purple"
            elif ball_colors_index_number == 10:
                ball_colors_index = "Brown"
            elif ball_colors_index_number == 11:
                ball_colors_index = "Orange"
            
            if paddle_colors_index_number == 0:
                paddle_colors_index = "Orange"
            elif paddle_colors_index_number == 1:
                paddle_colors_index = "Grey"
            elif paddle_colors_index_number == 2:
                paddle_colors_index = "White"
            elif paddle_colors_index_number == 3:
                paddle_colors_index = "Black"
            elif paddle_colors_index_number == 4:
                paddle_colors_index = "Blue"
            elif paddle_colors_index_number == 5:
                paddle_colors_index = "Dark Blue"
            elif paddle_colors_index_number == 6:
                paddle_colors_index = "Red"
            elif paddle_colors_index_number == 7:
                paddle_colors_index = "Yellow"
            elif paddle_colors_index_number == 8:
                paddle_colors_index = "Green"
            elif paddle_colors_index_number == 9:
                paddle_colors_index = "Pink"
            elif paddle_colors_index_number == 10:
                paddle_colors_index = "Purple"
            elif paddle_colors_index_number == 11:
                paddle_colors_index = "Brown"
            
            if os.path.exists(highscore):
                erasehighscorebutton = button(sc, (300, 580), "Erase Highscore")
            
            backtomainbutton = button(sc, (300, 650), "Back to Main")

            renderoptionstext = titlefont.render("Options", True, (255, 255, 255))
            sc.blit(renderoptionstext, (300, 30))
            
            rendersoundvolumetext = font2.render("Sound Volume", True, (255, 255, 255))
            sc.blit(rendersoundvolumetext, (300, 140))
            
            rendersoundvolumenumbertext = font2.render(str(soundvolumecounter), True, (255, 255, 255))
            sc.blit(rendersoundvolumenumbertext, (350, 190))
            
            rendersongvolumetext = font2.render("Song Volume", True, (255, 255, 255))
            sc.blit(rendersongvolumetext, (300, 235))
            
            rendersongvolumenumbertext = font2.render(str(songvolumecounter), True, (255, 255, 255))
            sc.blit(rendersongvolumenumbertext, (350, 277))

            renderspherecolortext = font2.render("Sphere Color", True, (255, 255, 255))
            sc.blit(renderspherecolortext, (300, 320))

            renderspherecolorindextext = font2.render(ball_colors_index, True, (255, 255, 255))
            sc.blit(renderspherecolorindextext, (375, 357))

            renderpaddlecolortext = font2.render("Paddle Color", True, (255, 255, 255))
            sc.blit(renderpaddlecolortext, (300, 400))

            renderpaddlecolorindextext = font2.render(paddle_colors_index, True, (255, 255, 255))
            sc.blit(renderpaddlecolorindextext, (375, 447))

            renderspherecoloradvicetext = font2.render("NOTE: White and Black colors will be difficult to see in bright", True, (255, 255, 255))
            sc.blit(renderspherecoloradvicetext, (300, 490))
            renderspherecoloradvicetext2 = font2.render("and dark ambient respectively.", True, (255, 255, 255))
            sc.blit(renderspherecoloradvicetext2, (300, 520))
        else:
            renderoptionstext = titlefont.render("Options", True, (255, 255, 255))
            sc.blit(renderoptionstext, (300, 30))

            renderareyousureerasehighscoretext = font2.render("Are you sure you want to erase your highscore? It can't be recovered back!", True, (255, 255, 255))
            sc.blit(renderareyousureerasehighscoretext, (300, 130))

            eraseconfirmbutton = button(sc, (300, 210), "Yes")
            erasenobutton = button(sc, (380, 210), "No")
    
    elif show_help_menu == True:
        #Introduction
        if helpindex == 1:
            helpindexsection = "Introduction"
            helpimg = pygame.image.load("assets/help/mainhelp.jpg").convert()
            helpimg = pygame.transform.scale(helpimg, (500, 500))
            renderhelptext = titlefont.render("Help", True, (255, 255, 255))
            sc.blit(renderhelptext, (300, 30))
            renderhelpfirstparttext = font2.render("Hello! It seems that you are beginner in this game.", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext, (580, 150))
            renderhelpfirstparttext2 = font2.render("So this Help section is more useful. We'll show you", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext2, (580, 180))
            renderhelpfirstparttext3 = font2.render("the basics of Breakout. To advance page, press Next", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext3, (580, 210))
            renderhelpfirstparttext4 = font2.render("button. To go back to previous page, press Previous", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext4, (580, 240))
            renderhelpfirstparttext5 = font2.render("button.", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext5, (580, 270))

            sc.blit(helpimg, (40, 120))
        #Brick
        elif helpindex == 2:
            helpindexsection = "Brick"
            helpimg = pygame.image.load("assets/help/blockhelp.jpg").convert()
            helpimg = pygame.transform.scale(helpimg, (500, 500))
            renderhelptext = titlefont.render("Help", True, (255, 255, 255))
            sc.blit(renderhelptext, (300, 30))
            renderhelpfirstparttext = font2.render("Do you see these things marked in red square here?", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext, (580, 150))
            renderhelpfirstparttext2 = font2.render("They are colored floating bricks. The goal of this", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext2, (580, 180))
            renderhelpfirstparttext3 = font2.render("game is to break all of them available in order to", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext3, (580, 210))
            renderhelpfirstparttext4 = font2.render("advance. If you break one brick, you gain more points", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext4, (580, 240))
            renderhelpfirstparttext5 = font2.render("that will be explained later. If you break all of bricks", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext5, (580, 270))
            renderhelpfirstparttext6 = font2.render("available in any levels, you'll pass to next level.", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext6, (580, 300))

            sc.blit(helpimg, (40, 120))
        #Ball
        elif helpindex == 3:
            helpindexsection = "Sphere"
            helpimg = pygame.image.load("assets/help/ballhelp.jpg").convert()
            helpimg = pygame.transform.scale(helpimg, (500, 500))
            renderhelptext = titlefont.render("Help", True, (255, 255, 255))
            sc.blit(renderhelptext, (300, 30))
            renderhelpfirstparttext = font2.render("As start point, there is a sphere. It is located at front", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext, (580, 150))
            renderhelpfirstparttext2 = font2.render("of paddle. It is useful for breaking bricks. To launch a", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext2, (580, 180))
            renderhelpfirstparttext3 = font2.render("sphere, you press Spacebar key. It is important that", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext3, (580, 210))
            renderhelpfirstparttext4 = font2.render("you take care of it. If you let it fall off screen,", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext4, (580, 240))
            renderhelpfirstparttext5 = font2.render("you lose one, this common mistake is related to", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext5, (580, 270))
            renderhelpfirstparttext6 = font2.render("concept that will be explained later.", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext6, (580, 300))

            sc.blit(helpimg, (40, 120))
        #Paddle movements
        elif helpindex == 4:
            helpindexsection = "Paddle movements"
            helpimg = pygame.image.load("assets/help/helppaddlemoveright.jpg").convert()
            helpimg = pygame.transform.scale(helpimg, (450, 250))
            helpimg2 = pygame.image.load("assets/help/helppaddlemoveleft.jpg").convert()
            helpimg2 = pygame.transform.scale(helpimg2, (450, 250))
            renderhelptext = titlefont.render("Help", True, (255, 255, 255))
            sc.blit(renderhelptext, (300, 30))
            renderhelpfirstparttext = font2.render("The paddle is useful for protecting spheres. To move", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext, (580, 150))
            renderhelpfirstparttext2 = font2.render("it to right, hold Right Arrow key. And to move it to", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext2, (580, 180))
            renderhelpfirstparttext3 = font2.render("left, hold Left Arrow key. So you'll don't have risk", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext3, (580, 210))
            renderhelpfirstparttext4 = font2.render("of losing spheres if doing in correct way.", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext4, (580, 240))

            sc.blit(helpimg, (40, 120))
            sc.blit(helpimg2, (40, 380))
        #Lives
        elif helpindex == 5:
            helpindexsection = "Lives"
            helpimg = pygame.image.load("assets/help/liveshelp.jpg").convert()
            helpimg = pygame.transform.scale(helpimg, (500, 500))
            renderhelptext = titlefont.render("Help", True, (255, 255, 255))
            sc.blit(renderhelptext, (300, 30))
            renderhelpfirstparttext = font2.render("There's 'Lives' located at the red sphere mark. When", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext, (580, 150))
            renderhelpfirstparttext2 = font2.render("you start the game, you begin with 4 lives left. Lives", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext2, (580, 180))
            renderhelpfirstparttext3 = font2.render("are number of spheres available to continue playing.", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext3, (580, 210))
            renderhelpfirstparttext4 = font2.render("As already said before, you lose more one life when", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext4, (580, 240))
            renderhelpfirstparttext5 = font2.render("you let sphere fall off screen. If you lose all lives,", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext5, (580, 270))
            renderhelpfirstparttext6 = font2.render("you don't have more chance to continue, resulting in", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext6, (580, 300))
            renderhelpfirstparttext7 = font2.render("game over, and you have to go back all from", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext7, (580, 330))
            renderhelpfirstparttext8 = font2.render("beginning.", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext8, (580, 360))

            sc.blit(helpimg, (40, 120))
        #Score
        elif helpindex == 6:
            helpindexsection = "Score"
            helpimg = pygame.image.load("assets/help/scorehelp.jpg").convert()
            helpimg = pygame.transform.scale(helpimg, (500, 500))
            renderhelptext = titlefont.render("Help", True, (255, 255, 255))
            sc.blit(renderhelptext, (300, 30))
            renderhelpfirstparttext = font2.render("Also, there's 'Score', who is very fundamental part", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext, (580, 150))
            renderhelpfirstparttext2 = font2.render("of this game. The more points you can reach, the", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext2, (580, 180))
            renderhelpfirstparttext3 = font2.render("better is your score. As already said before, you", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext3, (580, 210))
            renderhelpfirstparttext4 = font2.render("gain more 1000 points if you break one brick. If", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext4, (580, 240))
            renderhelpfirstparttext5 = font2.render("you gain every 100000 points, you gain one more", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext5, (580, 270))
            renderhelpfirstparttext6 = font2.render("life. That's interesting, isn't it?", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext6, (580, 300))

            sc.blit(helpimg, (40, 120))
        #Level
        elif helpindex == 7:
            helpindexsection = "Level"
            helpimg = pygame.image.load("assets/help/levelhelp.jpg").convert()
            helpimg = pygame.transform.scale(helpimg, (500, 500))
            renderhelptext = titlefont.render("Help", True, (255, 255, 255))
            sc.blit(renderhelptext, (300, 30))
            renderhelpfirstparttext = font2.render("So anyway, there's 'Level', who is also fundamental", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext, (580, 150))
            renderhelpfirstparttext2 = font2.render("part. The places, difficulty, number of bricks and", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext2, (580, 180))
            renderhelpfirstparttext3 = font2.render("sphere speed vary of level. The more you advance any", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext3, (580, 210))
            renderhelpfirstparttext4 = font2.render("level, more the difficulty, number of bricks and", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext4, (580, 240))
            renderhelpfirstparttext5 = font2.render("sphere speed will increase, and the place", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext5, (580, 270))
            renderhelpfirstparttext6 = font2.render("will change between themes such as city, forest,", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext6, (580, 300))
            renderhelpfirstparttext7 = font2.render("desert, ruins, sky, island, undersea, snow and space", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext7, (580, 330))

            sc.blit(helpimg, (40, 120))
        #Pausing game
        elif helpindex == 8:
            helpindexsection = "How to pause game"
            helpimg = pygame.image.load("assets/help/pausehelp.jpg").convert()
            helpimg = pygame.transform.scale(helpimg, (500, 500))
            renderhelptext = titlefont.render("Help", True, (255, 255, 255))
            sc.blit(renderhelptext, (300, 30))
            renderhelpfirstparttext = font2.render("To pause the game, press the 'P' key on keyboard.", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext, (580, 150))
            renderhelpfirstparttext2 = font2.render("This is more useful if you plan break time and you", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext2, (580, 180))
            renderhelpfirstparttext3 = font2.render("can't continue playing for while. Moreover, during", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext3, (580, 210))
            renderhelpfirstparttext4 = font2.render("the pause, you can change sound and song volumes,", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext4, (580, 240))
            renderhelpfirstparttext5 = font2.render("also present in 'Options' menu. You can also give", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext5, (580, 270))
            renderhelpfirstparttext6 = font2.render("up if you don't have desire to continue playing", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext6, (580, 300))
            renderhelpfirstparttext7 = font2.render("anymore. To resume the game, press the 'P' key", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext7, (580, 330))
            renderhelpfirstparttext8 = font2.render("again.", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext8, (580, 360))

            sc.blit(helpimg, (40, 120))
        #Conclusion
        elif helpindex == 9:
            helpindexsection = "Conclusion"
            helpimg = pygame.image.load("assets/help/mainhelp.jpg").convert()
            helpimg = pygame.transform.scale(helpimg, (500, 500))
            renderhelptext = titlefont.render("Help", True, (255, 255, 255))
            sc.blit(renderhelptext, (300, 30))
            renderhelpfirstparttext = font2.render("That's all for now! We hope that you feel ready and", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext, (580, 150))
            renderhelpfirstparttext2 = font2.render("you'll enjoy the game! To quit Help, click 'Back to", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext2, (580, 180))
            renderhelpfirstparttext3 = font2.render("Main' button. Good luck!", True, (255, 255, 255))
            sc.blit(renderhelpfirstparttext3, (580, 210))

            sc.blit(helpimg, (40, 120))

        helpbacktomainbutton = button(sc, (100, 660), "Back to Main")

        renderhelpindextext = font2.render(f"{str(helpindex)}/9", True, (255, 255, 255))
        sc.blit(renderhelpindextext, (760, 670))

        renderhelpindexsectiontext = font2.render(f"{helpindexsection}", True, (255, 255, 255))
        sc.blit(renderhelpindexsectiontext, (370, 670))

        if helpindex > 1:
            helppreviousbutton = button(sc, (580, 660), "Previous")
        
        if helpindex < 9:
            helpnextbutton = button(sc, (850, 660), "Next")

        pygame.display.update()
    
    #Update screen
    pygame.display.flip()
    clock.tick(fps)
