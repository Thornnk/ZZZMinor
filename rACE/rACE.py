import pygame
import os
import time
import random
pygame.init()

pygame.key.set_repeat(500, 100)
display_width, display_height = 800, 600
small_text, small_text2, small_text3 = pygame.font.Font('files\\fonts\\orange_juice_2.ttf', 30), \
    pygame.font.Font('files\\fonts\\playball.ttf', 50), pygame.font.Font('files\\fonts\\lato.ttf', 20),
medium_text, large_text, title_text = pygame.font.Font('files\\fonts\\coaster_quake.otf', 230), \
    pygame.font.Font('files\\fonts\\orange_juice_2.ttf', 100), pygame.font.Font('files\\fonts\\orange_juice_2.ttf', 250)
black, white, grey, light_grey, dark_grey, red, green, \
    dark_green, green_pale, blue, light_blue, yellow, brown, purple, \
    light_purple, lighter_purple = \
    (0, 0, 0), (255, 255, 255), (100, 100, 100), (180, 180, 180), (64, 64, 64), (255, 0, 0), (0, 255, 0), \
    (0, 100, 0), (153, 255, 153), (0, 0, 255), (0, 255, 255), (255, 255, 0), (153, 76, 0), (76, 0, 153), \
    (178, 102, 255), (204, 153, 255)

os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
pygame.display.set_caption('rACE')
pause = False
name = ''
speed = 0
score = 0
high_score = -1

# Sound
menu_music = 'files\\sounds\\menu.ogg'
race_music = 'files\\sounds\\race.ogg'
gameover_music = 'files\\sounds\\gameover.ogg'
click_sound = pygame.mixer.Sound('files\\sounds\\click.ogg')
pause_sound = pygame.mixer.Sound('files\\sounds\\pause.ogg')
engine_sound = pygame.mixer.Sound('files\\sounds\\engine.ogg')
accel_sound = pygame.mixer.Sound('files\\sounds\\accel.ogg')
maxspeed_sound = pygame.mixer.Sound('files\\sounds\\maxspeed.ogg')
screech_sound = pygame.mixer.Sound('files\\sounds\\screech.ogg')
crash_sound = pygame.mixer.Sound('files\\sounds\\crash.ogg')
mute, check = False, False

# Backgrounds
menu_bg = pygame.image.load('files\\images\\menu_bg.jpg').convert()
pygame.display.set_icon(pygame.image.load('files\\images\\wheel.png').convert_alpha())
ibg_w, ibg_h = menu_bg.get_rect().width, menu_bg.get_rect().height
game_bg = pygame.image.load('files\\images\\game_bg.jpg').convert()
bg_w, bg_h = game_bg.get_rect().width, game_bg.get_rect().height
r_border, l_border = 50, 50

# Images
tyres = pygame.image.load('files\\images\\tyres.png').convert_alpha()
flag_l = pygame.image.load('files\\images\\flag_l.png').convert_alpha()
flag_r = pygame.image.load('files\\images\\flag_r.png').convert_alpha()
carImg = pygame.image.load('files\\images\\car.png')
car_l3 = pygame.image.load('files\\images\\car_l3.png')
car_r3 = pygame.image.load('files\\images\\car_r3.png')
car_x, car_y, car_width, car_height = (display_width * 0.45), (display_height * 0.8), 50, 100
box1 = pygame.image.load('files\\images\\null.png').convert()
box2 = pygame.image.load('files\\images\\null.png').convert()
box_1, box_2, box_3, box_4 = \
    pygame.image.load('files\\images\\box1.png').convert(), pygame.image.load('files\\images\\box2.png').convert(), \
    pygame.image.load('files\\images\\box3.png').convert(), pygame.image.load('files\\images\\box4.png').convert()
box_x1, box_y1, box_width1, box_height1 = 0, 0, 0, 0
box_x2, box_y2, box_width2, box_height2 = 0, 0, 0, 0

explosion = pygame.image.load('files\\images\\explosion.png').convert_alpha()
smoke = pygame.image.load('files\\images\\smoke.png')


def player_name():
    global name, mute, check
    input_box = pygame.Rect(display_width * 0.5, display_height * 0.8, 50, 32)
    ic = light_purple
    ac = lighter_purple
    box_color = ac
    active = True
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                box_color = ac if active else ic
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if name == '':
                            name_error()
                        else:
                            print(name)
                            done = True
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]

                    elif event.key == pygame.K_m:
                        mods = pygame.key.get_mods()
                        if mods & pygame.KMOD_CTRL:
                            mute = not mute
                            check = True
                    elif event.unicode.isalpha():
                        if len(name) < 20:
                            if event.unicode == 20:
                                name += 0
                            else:
                                name += event.unicode
                    # else:
                    #     name += event.unicode

                if not active:
                    if event.key == pygame.K_m:
                        mods = pygame.key.get_mods()
                        if mods & pygame.KMOD_CTRL:
                            mute = not mute
                            check = True
            if check == 1:
                if mute:
                    pygame.mixer.music.stop()
                    check = False
                else:
                    pygame.mixer.music.load(menu_music)
                    pygame.mixer.music.play(-1)
                    check = False

            pygame.display.update()
            clock.tick(30)

        screen.blit(menu_bg, (0, 0))
        text_surf, text_rect = text_obj('rACE', title_text, purple)
        text_rect.center = ((display_width * 0.5), (display_height * 0.22))
        screen.blit(text_surf, text_rect)

        screen.blit(tyres, (0, 290))

        input_name = small_text2.render('Input your name:', True, green, grey)
        input_name_rect = input_name.get_rect(center=(display_width * 0.5, display_height * 0.5))
        text_surf, text_rect = input_name, input_name_rect
        text_rect.center = ((display_width * 0.5), (display_height * 0.62))
        screen.blit(text_surf, text_rect)

        input_box.center = (display_width*0.5, display_height*0.75)
        pygame.draw.rect(screen, box_color, input_box)
        pygame.draw.rect(screen, purple, input_box, 2)
        text_surf = pygame.font.Font('files\\fonts\\playball.ttf', 30).render(name, True, black)
        text_rect = text_surf.get_rect()
        text_rect.center = (display_width*0.5, display_height*0.75)
        input_box.w = text_rect.w + 50
        screen.blit(text_surf, text_rect)

        button('Accept', 350, 505, 100, 30, light_purple, lighter_purple, 'accept')

        pygame.display.update()
        clock.tick(30)

    game_menu()


def name_error():
    global mute, check
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    player_name()
                if event.key == pygame.K_m:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        mute = not mute
                        check = True
            if check == 1:
                if mute:
                    pygame.mixer.music.stop()
                    check = False
                else:
                    pygame.mixer.music.load(menu_music)
                    pygame.mixer.music.play(-1)
                    check = False

        popup = pygame.Rect(display_width * 0.5, display_height * 0.5, 600, 200)
        popup.center = (display_width * 0.5, display_height * 0.73)
        pygame.draw.rect(screen, light_grey, popup)
        pygame.draw.rect(screen, grey, popup, 4)
        text_surf, text_rect = text_obj('Please enter a name', pygame.font.Font('files\\fonts\\lato.ttf', 60), red)
        text_rect.center = ((display_width*0.5), (display_height*0.65))
        screen.blit(text_surf, text_rect)

        button('Understood', 325, 450, 150, 60, light_purple, lighter_purple, 'understood')

        pygame.display.update()
        clock.tick(30)


def score_p(count):
    font = pygame.font.Font('files\\fonts\\comic.ttf', 18)
    text = font.render('Score: ' + str(count), True, green)
    screen.blit(text, (display_width - 100, 5))


def new_box1():
    global box1, box_x1, box_y1, box_width1, box_height1

    size = 0
    while True:
        if size == 0:
            size = random.randrange(1, 5)
        elif size == 1:
            box1 = box_1
            box_width1 = box_1.get_rect().width
            box_height1 = box_1.get_rect().height
            break
        elif size == 2:
            box1 = box_2
            box_width1 = box_2.get_rect().width
            box_height1 = box_2.get_rect().height
            break
        elif size == 3:
            box1 = box_3
            box_width1 = box_3.get_rect().width
            box_height1 = box_3.get_rect().height
            break
        elif size == 4:
            box1 = box_4
            box_width1 = box_4.get_rect().width
            box_height1 = box_4.get_rect().height
            break
    box_x1, box_y1 = (random.randrange(l_border, display_width - r_border - box_width1)), -box_height1


def new_box2():
    global box2, box_x2, box_y2, box_width2, box_height2

    size = 0
    while True:
        if size == 0:
            size = random.randrange(1, 5)
        elif size == 1:
            box2 = box_1
            box_width2 = box_1.get_rect().width
            box_height2 = box_1.get_rect().height
            break
        elif size == 2:
            box2 = box_2
            box_width2 = box_2.get_rect().width
            box_height2 = box_2.get_rect().height
            break
        elif size == 3:
            box2 = box_3
            box_width2 = box_3.get_rect().width
            box_height2 = box_3.get_rect().height
            break
        elif size == 4:
            box2 = box_4
            box_width2 = box_4.get_rect().width
            box_height2 = box_4.get_rect().height
            break
    box_x2, box_y2 = (random.randrange(l_border, display_width - r_border - box_width2)), -box_height2


def car(x, y):
    screen.blit(carImg, (x, y))


def text_press(text):
    text_obj(text, small_text, blue)


def text_obj(text, font, tcolor):
    text_surface = font.render(text, True, tcolor)
    return text_surface, text_surface.get_rect(center=(display_width*0.5, display_height*0.5))


def explosion_f():
    exp_rect = explosion.get_rect()
    frames_number = 26
    frame_width, frame_height = exp_rect.width / frames_number, exp_rect.height
    frames_list = list([(frame_width * frame, 0, frame_width, frame_height) for frame in range(frames_number)])
    frame = 0
    exp = True
    while exp:
        screen.blit(explosion, (car_x-25, car_y-5), frames_list[frame])
        frame += 1
        if frame > frames_number-1:
            screen.blit(smoke, (car_x - 50, car_y - 25))
            exp = False
        pygame.display.update()
        clock.tick(30)


def crash():
    global mute, check, score, high_score
    pygame.mixer.stop()
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    explosion_f()

    text_surf, text_rect = text_obj('YOU CRASHED', medium_text, red)
    text_rect.center = ((display_width / 2), (display_height / 3))
    screen.blit(text_surf, text_rect)
    pygame.display.update()

    pygame.mouse.set_visible(True)
    pygame.mixer.music.load(gameover_music)
    pygame.mixer.music.play(-1, 15000)

    if score > high_score:
        high_score = score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        mute = not mute
                        check = True
            if check == 1:
                if mute:
                    pygame.mixer.music.stop()
                    check = False
                else:
                    pygame.mixer.music.load(gameover_music)
                    pygame.mixer.music.play(-1)
                    check = False
        button('Play Again', ((display_width*0.25)-75), ((display_height*0.75)-25), 200, 50, grey, light_grey, 'play')
        button('Menu', ((display_width*0.75)-50), ((display_height*0.75)-25), 200, 50, grey, light_grey, 'main_menu')

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, width, height, ic, ac, action=None):
    global name, check
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(screen, ic, (x, y, width, height))
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x+4, y+4, width-8, height-8))
        if click[0] == 1 and action is not None:
            if action == 'main_menu':
                pygame.mixer.Sound.play(click_sound)
                main_menu()
            if action == 'game_menu':
                pygame.mixer.Sound.play(click_sound)
                game_menu()
            if action == 'play':
                pygame.mixer.music.stop()
                game_loop()
            if action == 'continue':
                pygame.mixer.Sound.play(click_sound)
                unpaused()
            if action == 'high_score_screen':
                pygame.mixer.Sound.play(click_sound)
                high_score_screen()
            if action == 'new_player':
                name = ''
                pygame.mixer.Sound.play(click_sound)
                player_name()
            if action == 'accept':
                pygame.mixer.Sound.play(click_sound)
                if name == '':
                    name_error()
                else:
                    game_menu()
            if action == 'understood':
                pygame.mixer.Sound.play(click_sound)
                player_name()
            if action == 'quit':
                pygame.mixer.Sound.play(click_sound)
                quit_game()

    if msg == 'GO!':
        screen.blit(flag_l, (x + 10, y + 15))
        screen.blit(flag_r, (x + width - 36, y + 15))
    if msg == 'New player' or msg == 'Accept' or msg == 'Understood':
        text_surf, text_rect = text_obj(msg, pygame.font.Font('files\\fonts\\orange_juice_2.ttf', 22), black)
        text_rect.center = (x + (width / 2), y + (height / 2))
        screen.blit(text_surf, text_rect)
    else:
        text_surf, text_rect = text_obj(msg, small_text, black)
        text_rect.center = (x + (width/2), y + (height/2))
        screen.blit(text_surf, text_rect)


def unpaused():
    global pause
    pygame.mouse.set_visible(False)
    pause = False
    pygame.mixer.music.unpause()
    maxspeed_sound.play(-1)


def paused():
    global mute, check
    pygame.mixer.pause()
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(pause_sound)
    pygame.mouse.set_visible(True)

    text_surf, text_rect = text_obj('Paused', pygame.font.Font('files\\fonts\\mocking_bird.otf', 180), purple)
    text_rect.center = ((display_width / 2), (display_height / 3))
    screen.blit(text_surf, text_rect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    unpaused()
                if event.key == pygame.K_m:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        mute = not mute
                        check = True
            if check == 1:
                if mute:
                    pygame.mixer.music.stop()
                    check = False
                else:
                    pygame.mixer.music.load(menu_music)
                    pygame.mixer.music.play(-1)
                    check = False

        button('Continue', ((display_width*0.25)-75), ((display_height*0.75)-25), 150, 50, grey, light_grey, 'continue')
        button('Menu', ((display_width*0.75)-50), ((display_height*0.75)-25), 150, 50, grey, light_grey, 'main_menu')

        pygame.display.update()
        clock.tick(15)


def quit_game():
    pygame.quit()
    quit()


def high_score_screen():
    global name, mute, check
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        mute = not mute
                        check = True
            if check == 1:
                if mute:
                    pygame.mixer.music.stop()
                    check = False
                else:
                    pygame.mixer.music.load(menu_music)
                    pygame.mixer.music.play(-1)
                    check = False

        screen.blit(menu_bg, (0, 0))
        pygame.draw.rect(screen, lighter_purple, (30, 30, 740, 540))

        text_surf, text_rect = text_obj('High Score', large_text, purple)
        text_rect.center = ((display_width*0.5), (display_height*0.15))
        screen.blit(text_surf, text_rect)

        button('Back', ((display_width*0.5)-100), ((display_height*0.9)-25), 200, 50, grey, light_grey, 'game_menu')

        if high_score >= 0:
            content = '%s %s %s' % (name, '.'*100, high_score)
            text_surf, text_rect = text_obj(str(content), small_text3, purple)
            text_rect.center = ((display_width*0.5), (display_height*0.5))
            screen.blit(text_surf, text_rect)

        pygame.display.update()
        clock.tick(15)


def name_menu():
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)
    player_name()


def main_menu():
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)
    game_menu()


def game_menu():
    global mute, check
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        mute = not mute
                        check = True
            if check == 1:
                if mute:
                    pygame.mixer.music.stop()
                    check = False
                else:
                    pygame.mixer.music.load(menu_music)
                    pygame.mixer.music.play(-1)
                    check = False

        screen.blit(menu_bg, (0, 0))
        text_surf, text_rect = text_obj('rACE', title_text, purple)
        text_rect.center = ((display_width*0.5), (display_height*0.22))
        screen.blit(text_surf, text_rect)

        button('GO!', ((display_width*0.5)-100), ((display_height*0.6)-25), 200, 50, grey, light_grey, 'play')
        button('High Score', ((display_width*0.5)-100), ((display_height*0.7)-25), 200, 50, grey, light_grey,
               'high_score_screen')
        button('Quit', ((display_width*0.5)-100), ((display_height*0.8)-25), 200, 50, grey, light_grey, 'quit')
        button('New player', display_width-170, display_height-50, 150, 30, light_purple, lighter_purple, 'new_player')

        text_surf, text_rect = text_obj('Welcome %s!' % name, pygame.font.Font('files\\fonts\\playball.ttf', 25),
                                        purple)
        text_rect = (20, 555)
        screen.blit(text_surf, text_rect)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global pause, score, mute, check, car_x, car_y, speed
    global box1, box_x1, box_y1, box_width1, box_height1, box2, box_x2, box_y2, box_width2, box_height2
    pygame.mouse.set_visible(False)

    pygame.mixer.Sound.play(engine_sound)
    time.sleep(1)
    pygame.mixer.music.load(race_music)
    pygame.mixer.music.play(-1)
    pygame.mixer.Sound.play(accel_sound)
    maxspeed_sound.play(-1, 0, 12000)

    car_x, car_y = (display_width * 0.45), (display_height * 0.8)
    car_x_change = 0
    speed = 4
    score = 0
    bg_y = 0
    bg_y2 = -bg_h
    init_box = 1
    speed_b2 = 0
    l3, r3 = 0, 0

    game_running = True
    while game_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    r3 = 0
                    l3 = 1
                    pygame.mixer.Sound.play(screech_sound, -1)
                    car_x_change = -5
                if event.key == pygame.K_LEFT and event.key == pygame.K_RIGHT or \
                        event.key == pygame.K_a and event.key == pygame.K_d:
                    r3 = 0
                    l3 = 1
                    pygame.mixer.Sound.play(screech_sound, -1)
                    car_x_change = -5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    l3 = 0
                    r3 = 1
                    pygame.mixer.Sound.play(screech_sound, -1)
                    car_x_change = 5
                if event.key == pygame.K_RIGHT and event.key == pygame.K_LEFT or \
                        event.key == pygame.K_d and event.key == pygame.K_a:
                    l3 = 0
                    r3 = 1
                    pygame.mixer.Sound.play(screech_sound, -1)
                    car_x_change = 5
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_m:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        mute = not mute
                        check = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or \
                        event.key == pygame.K_d:
                    l3, r3 = 0, 0
                    pygame.mixer.Sound.fadeout(screech_sound, 500)
                    car_x_change = 0
            if check == 1:
                if mute:
                    pygame.mixer.music.stop()
                    check = False
                else:
                    pygame.mixer.music.load(race_music)
                    pygame.mixer.music.play(-1)
                    check = False

    # Background
        car_x += car_x_change

        screen.blit(game_bg, (0, bg_y))
        screen.blit(game_bg, (0, bg_y2))
        if bg_y > bg_h:
            bg_y = -bg_h
        if bg_y2 > bg_h:
            bg_y2 = -bg_h

        bg_y += speed
        bg_y2 += speed

    # Obstacles
        if init_box == 1:
            new_box1()
            new_box2()
            box_y2 = display_height+1
            init_box = 0
        if (display_height*0.5)+50 > box_y1+(box_height1*0.5) > display_height*0.5:
            speed_b2 = 1
            if box_y2 > display_height:
                rand = random.randrange(0, 2)
                if rand == 1 or rand == 2:
                    speed_b2 = 1
        if box_y1 > display_height:
            new_box1()
            speed += 0.2
        if box_y2 > display_height:
            speed_b2 = 0
            new_box2()
        screen.blit(box1, (box_x1, box_y1))
        screen.blit(box2, (box_x2, box_y2))
        box_y1 += speed
        if speed_b2 == 1:
            box_y2 += speed

    # Other objects
        score_p(score)
        if l3 == 1:
            screen.blit(car_l3, (car_x, car_y))
        elif r3 == 1:
            screen.blit(car_r3, (car_x, car_y))
        else:
            car(car_x, car_y)

    # Crash
        if car_x > (display_width-r_border-car_width) or car_x < l_border:
            crash()
        if car_y < box_y1 + box_height1:
            if box_x1+box_width1 > car_x > box_x1 or box_x1 < car_x+car_width < box_x1+box_width1:
                crash()
        if car_y < box_y2 + box_height2:
            if box_x2+box_width2 > car_x > box_x2 or box_x2 < car_x+car_width < box_x2+box_width1:
                crash()

        if box_y1 > display_height or box_y2 > display_height:
            score += 1

        pygame.display.update()
        clock.tick(60)


name_menu()
quit_game()
