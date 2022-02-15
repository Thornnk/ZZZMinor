import turtle
import pygame
import random
import time

pygame.init()
scr = turtle.Screen()
scr.title('Th\'s Pong')
scr.bgcolor('#032603')
scr.setup(width=800, height=600)
scr.tracer(0)
paddle_sound = pygame.mixer.Sound('paddle.ogg')
score_sound = pygame.mixer.Sound('score.ogg')
wall_sound = pygame.mixer.Sound('wall.ogg')


def pass_intro():
    global run
    run = False


def pass_intro2(x, y):
    x+y
    global run
    run = False


title = turtle.Turtle()
title.speed(0)
title.color('red')
title.penup()
title.hideturtle()
title.goto(10, -140)
run = True
while run:
    title.write('Welcome\nTH\'S PONG!', align='center', font=('Luna', 50, 'normal'))
    scr.listen()
    scr.onkeypress(pass_intro, 'space')
    scr.onclick(pass_intro2)
title.clear()

# Score
score_a = 0
score_b = 0
a_s, b_s = 0, 0

# Basic definitions                     <---- ## Modify here first
scr_width = 800
scr_height = 600
border = 20
sep_height = 60
table_center = (0, -30)
paddle_speed = 10
paddle_w_multiplier, paddle_h_multiplier = 0.5, 3
paddle_width, paddle_height = 20*paddle_w_multiplier, 20*paddle_h_multiplier
ball_multiplier = 0.5
ball_r = 10*0.5


# Table lines
sep = turtle.Turtle()
sep.speed(0)
sep.hideturtle()
sep.penup()
sep.begin_fill()
sep.goto(-scr_width*0.5, scr_height*0.5)
sep.forward(scr_width)
sep.right(90)
sep.forward(sep_height)
sep.right(90)
sep.forward(scr_width)
sep.right(90)
sep.forward(sep_height)
sep.color('#18b842')
sep.penup()
sep.end_fill()

rect = turtle.Turtle()
rect.speed(0)
rect.color('white')
rect.hideturtle()
rect.penup()
rect.goto((-scr_width*0.5)+border+paddle_width, (scr_height*0.5)-sep_height-border)
rect.pendown()
rect.forward(scr_width-border-paddle_width-paddle_width-border)
rect.right(90)
rect.forward(scr_height-sep_height-border-border)
rect.right(90)
rect.forward(scr_width-border-paddle_width-paddle_width-border)
rect.right(90)
rect.forward(scr_height-sep_height-border-border)
rect.penup()
rect.goto(-scr_width*0.5+border+paddle_width, -sep_height*0.5)
rect.pendown()
rect.goto(scr_width*0.5-border-paddle_width, -sep_height*0.5)
rect.penup()

net = turtle.Turtle()
net.speed()
net.shape('square')
net.shapesize(stretch_wid=(scr_height-sep_height-border-border)*0.05, stretch_len=0.2)
net.color('white')
net.penup()
net.goto(table_center)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape('square')
paddle_a.shapesize(stretch_wid=paddle_h_multiplier, stretch_len=paddle_w_multiplier)
paddle_a.color('white')
paddle_a.penup()
paddle_a.goto(-375, -30)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape('square')
paddle_b.shapesize(stretch_wid=paddle_h_multiplier, stretch_len=paddle_w_multiplier)
paddle_b.color('white')
paddle_b.penup()
paddle_b.goto(375, -30)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape('circle')
ball.shapesize(stretch_wid=ball_multiplier, stretch_len=ball_multiplier)
ball.color('white')
ball.penup()
ball.goto(table_center)
ball.dx = 0
ball.dy = 0

# Score text
text_score_a = turtle.Turtle()
text_score_a.speed(0)
text_score_a.color('white')
text_score_a.penup()
text_score_a.hideturtle()
text_score_a.goto(-scr_width*0.5*0.5, scr_height*0.5-sep_height*0.80)
text_score_a.write('Player A:  %i' % score_a, align='center', font=('Luna', 12, 'normal'))

text_score_b = turtle.Turtle()
text_score_b.speed(0)
text_score_b.color('white')
text_score_b.penup()
text_score_b.hideturtle()
text_score_b.goto(scr_width*0.5*0.5, scr_height*0.5-sep_height*0.80)
text_score_b.write('Player B:  %i' % score_b, align='center', font=('Luna', 12, 'normal'))


# Functions
def paddle_a_up():
    y = paddle_a.ycor()
    if y < scr_height*0.5-sep_height-border-paddle_height*0.5:
        y += paddle_speed
        paddle_a.sety(y)
    else:
        paddle_a.sety(scr_height*0.5-sep_height-border-paddle_height*0.5)


def paddle_a_down():
    y = paddle_a.ycor()
    if -scr_height*0.5+border+paddle_height*0.5 < y:
        y += -paddle_speed
        paddle_a.sety(y)
    else:
        paddle_a.sety(-scr_height*0.5+border+paddle_height*0.5)


def paddle_b_up():
    y = paddle_b.ycor()
    if y < scr_height*0.5-sep_height-border-paddle_height*0.5:
        y += paddle_speed
        paddle_b.sety(y)
    else:
        paddle_b.sety(scr_height*0.5-sep_height-border-paddle_height*0.5)


def paddle_b_down():
    y = paddle_b.ycor()
    if -scr_height*0.5+border+paddle_height*0.5 < y:
        y += -paddle_speed
        paddle_b.sety(y)
    else:
        paddle_b.sety(-scr_height*0.5+border+paddle_height*0.5)


def reset_ball():
    global a_s, b_s
    ball.goto(table_center)
    if a_s == 1:
        ball.dx = -1
        a_s = 0
        rand = random.randrange(0, 2)
        if rand == 1:
            ball.dy = -1
        else:
            ball.dy = 1
    elif b_s == 1:
        ball.dx = 1
        b_s = 0
        rand = random.randrange(0, 2)
        if rand == 1:
            ball.dy = -1
        else:
            ball.dy = 1
    else:
        rand = random.randrange(0, 2)
        if rand == 1:
            ball.dx = -1
            rand1 = random.randrange(0, 2)
            if rand1 == 1:
                ball.dy = -1
            else:
                ball.dy = 1
        else:
            ball.dx = 1
            rand2 = random.randrange(0, 2)
            if rand2 == 1:
                ball.dy = -1
            else:
                ball.dy = 1


def on_close():
    global running
    running = False


# Key binding
scr.listen()
scr.onkeypress(paddle_a_up, 'w')
scr.onkeypress(paddle_a_down, 's')
scr.onkeypress(paddle_b_up, 'Up')
scr.onkeypress(paddle_b_down, 'Down')
scr.onkeypress(reset_ball, 'space')

canvas = scr.getcanvas()
root = canvas.winfo_toplevel()
root.protocol("WM_DELETE_WINDOW", on_close)

# Game Loop
running = True
while running:
    # Ball moving
    ball.setx(ball.xcor()+ball.dx)
    ball.sety(ball.ycor()+ball.dy)

    # Borders
    if ball.ycor() > scr_height*0.5-sep_height-border-ball_r:
        ball.sety(scr_height*0.5-sep_height-border-ball_r)
        pygame.mixer.Sound.play(wall_sound)
        ball.dy = -ball.dy
    if ball.ycor() < -scr_height*0.5+border+ball_r:
        ball.sety(-scr_height*0.5+border+ball_r)
        pygame.mixer.Sound.play(wall_sound)
        ball.dy = -ball.dy

    if ball.xcor() > scr_width*0.5:
        pygame.mixer.Sound.play(score_sound)
        score_a += 1
        text_score_a.clear()
        text_score_a.write('Player A:  %i' % score_a, align='center', font=('Luna', 12, 'normal'))
        ball.dx, ball.dy = 0, 0
        a_s = 1
        ball.goto(table_center)
    if ball.xcor() < -scr_width*0.5:
        pygame.mixer.Sound.play(score_sound)
        score_b += 1
        text_score_b.clear()
        text_score_b.write('Player B:  %i' % score_b, align='center', font=('Luna', 12, 'normal'))
        ball.dx, ball.dy = 0, 0
        b_s = 1
        ball.goto(table_center)

    # Paddle collision
    if paddle_a.ycor()-paddle_height*0.5-ball_r < ball.ycor() < paddle_a.ycor()+paddle_height*0.5+ball_r and \
            paddle_a.xcor()+paddle_width*0.5+ball_r-2 < ball.xcor() < paddle_a.xcor()+paddle_width*0.5+ball_r:
        ball.setx(paddle_a.xcor()+paddle_width*0.5+ball_r)
        pygame.mixer.Sound.play(paddle_sound)
        ball.dx = -ball.dx
    if paddle_a.xcor()-paddle_width*0.5-ball_r < ball.xcor() < paddle_a.xcor()+paddle_width*0.5+ball_r:
        if paddle_a.ycor()+paddle_height*0.5+ball_r-2 < ball.ycor() < paddle_a.ycor()+paddle_height*0.5+ball_r:
            ball.sety(paddle_a.ycor()+paddle_height*0.5+ball_r)
            pygame.mixer.Sound.play(paddle_sound)
            ball.dy = -ball.dy
        if paddle_a.ycor()-paddle_height*0.5-ball_r < ball.ycor() < paddle_a.ycor()-paddle_height*0.5-ball_r+2:
            ball.sety(paddle_a.ycor()-paddle_height*0.5-ball_r)
            pygame.mixer.Sound.play(paddle_sound)
            ball.dy = -ball.dy

    if paddle_b.ycor()-paddle_height*0.5-ball_r < ball.ycor() < paddle_b.ycor()+paddle_height*0.5+ball_r and \
            paddle_b.xcor()-paddle_width*0.5-ball_r < ball.xcor() < paddle_b.xcor()-paddle_width*0.5-ball_r+2:
        ball.setx(paddle_b.xcor()-paddle_width*0.5-ball_r)
        pygame.mixer.Sound.play(paddle_sound)
        ball.dx = -ball.dx
    if paddle_b.xcor()-paddle_width*0.5-ball_r < ball.xcor() < paddle_b.xcor()+paddle_width*0.5+ball_r:
        if paddle_b.ycor()+paddle_height*0.5+ball_r-2 < ball.ycor() < paddle_b.ycor()+paddle_height*0.5+ball_r:
            ball.sety(paddle_b.ycor()+paddle_height*0.5+ball_r)
            pygame.mixer.Sound.play(paddle_sound)
            ball.dy = -ball.dy
        if paddle_b.ycor()-paddle_height*0.5-ball_r < ball.ycor() < paddle_b.ycor()-paddle_height*0.5-ball_r+2:
            ball.sety(paddle_b.ycor()-paddle_height*0.5-ball_r)
            pygame.mixer.Sound.play(paddle_sound)
            ball.dy = -ball.dy

    scr.update()
    time.sleep(0.005)
