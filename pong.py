import pygame 
import random 
import time
import math

pygame.init()

WIDTH, HEIGHT = 1000, 600
GAME_WIN = pygame.display.set_mode((WIDTH, HEIGHT))
START_WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

COLOR = (224, 224, 224)
BG_COLOR = (0, 25, 40)
BAR_HEIGHT = 100
BAR_WIDTH = 20
BALL_RADIUS = 20
SPEED = 4
FONT_SIZE = 40
LABEL_FONT = pygame.font.SysFont("copperplate gothic bold", 30)
TITLE_FONT = pygame.font.SysFont("copperplate gothic bold", 50)
OPTIONS_FONT = pygame.font.SysFont("copperplate gothic bold", FONT_SIZE)

class Bar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        
    def draw_bar(self, win):
        pygame.draw.rect(win, COLOR, (self.x, self.y, BAR_WIDTH, BAR_HEIGHT))

    def bar_movement_1(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.y >= 0:
            self.y -= SPEED
        if keys[pygame.K_s] and self.y <= HEIGHT - BAR_HEIGHT:
            self.y += SPEED

    def bar_movement_2(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.y >= 0:
            self.y -= SPEED
        if keys[pygame.K_DOWN] and self.y <= HEIGHT - BAR_HEIGHT:
            self.y += SPEED

    def automate(self, ball):
        if ball.y <= self.y:
            self.y -= SPEED
        if ball.y >= self.y + BAR_HEIGHT:
            self.y += SPEED

class Ball:
    BALL_SPEED = 8

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_dir = self.BALL_SPEED * random.randrange(-1, 2, 2)
        self.x_dir = self.BALL_SPEED * random.randrange(-1, 2, 2)

    def draw_ball(self, win):
        pygame.draw.circle(win, COLOR, (self.x, self.y), BALL_RADIUS)

    def ball_movement(self):
        self.x += self.x_dir
        self.y += self.y_dir

    def collision(self, player_1, player_2):
        if self.y <= BALL_RADIUS:
            self.y_dir *= -1
        if self.y + BALL_RADIUS >= HEIGHT:
            self.y_dir *= -1
        if self.x - BALL_RADIUS <= player_1.x + BAR_WIDTH and player_1.y <= self.y <= player_1.y + BAR_HEIGHT:
            self.x_dir = self.BALL_SPEED
        if self.x + BALL_RADIUS >= player_2.x and player_2.y <= self.y <= player_2.y + BAR_HEIGHT:
            self.x_dir = -self.BALL_SPEED

    def reset(self):
        self.x, self.y = WIDTH/2, HEIGHT/2
        self.x_dir = 0
        self.y_dir = 0


class Label:
    def __init__(self, x, y, text):
        self.text = text
        self.label = OPTIONS_FONT.render(self.text, 1, COLOR)
        self.width = self.label.get_rect()[2] 
        self.height = self.label.get_rect()[3]
        self.x = x - self.width/2
        self.y = y - self.height/2

    def draw_label(self, win):
        win.blit(self.label, (self.x, self.y))

    def is_pressed(self, x, y):
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True

def draw(win, player_1, player_2, ball):
    win.fill(BG_COLOR)
    pygame.draw.line(win, COLOR, (WIDTH/2, 0), (WIDTH/2, HEIGHT))
    player_1.draw_bar(win)
    player_2.draw_bar(win)
    ball.draw_ball(win)
    draw_score(win, player_1, player_2)

def draw_score(win, player_1, player_2):
    player_1_score = LABEL_FONT.render(f"Player 1: {player_1.score}", 1, COLOR)
    player_2_score = LABEL_FONT.render(f"Player 2: {player_2.score}", 1, COLOR)

    win.blit(player_1_score, (WIDTH/2 - 120, 10))
    win.blit(player_2_score, (WIDTH/2 + 20, 10))

def start():
    run = True 
    quit = False
    start = False
    clock = pygame.time.Clock()
    title_label = Label(WIDTH/2, 80, "PONG")
    start_label = Label(WIDTH/2, 210, "Please select a game mode to start")
    single_label = Label(WIDTH/2, 330, "Single Player")
    multi_label = Label(WIDTH/2, 430, "Multiplayer")

    while run:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        single = single_label.is_pressed(*mouse_pos)
        multi = multi_label.is_pressed(*mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN and (single or multi):
                run = False
                start = True
                break

        GAME_WIN.fill(BG_COLOR)
        title_label.draw_label(GAME_WIN)
        start_label.draw_label(GAME_WIN)
        single_label.draw_label(GAME_WIN)
        multi_label.draw_label(GAME_WIN)

        pygame.display.update()

    if quit:
        pygame.quit()

    elif start and single:
        main(True)

    elif start and multi:
        main(False)

def main(automate):
    run = True
    clock = pygame.time.Clock()
    player_1 = Bar(50, HEIGHT/2 - BAR_HEIGHT/2)
    player_2 = Bar(WIDTH - 50 - BAR_WIDTH, HEIGHT/2 - BAR_HEIGHT/2)
    ball = Ball(WIDTH/2, HEIGHT/2)
    time_initial = time.time()

    while run:
        clock.tick(60)
        elapsed_time = math.floor(time.time() - time_initial)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(GAME_WIN, player_1, player_2, ball)

        if elapsed_time < 3:
            counter_1 = Label(120, HEIGHT/2, str(3 - elapsed_time))
            counter_2 = Label(WIDTH - 120, HEIGHT/2, str(3 - elapsed_time))
            counter_1.draw_label(GAME_WIN)
            counter_2.draw_label(GAME_WIN)

        elif elapsed_time == 3:
            counter_1 = Label(120, HEIGHT/2, "GO!")
            counter_2 = Label(WIDTH - 120, HEIGHT/2, "GO!")
            counter_1.draw_label(GAME_WIN)
            counter_2.draw_label(GAME_WIN)
    
        if ball.x <= player_1.x:
            player_1.y, player_2.y = HEIGHT/2 - BAR_HEIGHT/2, HEIGHT/2 - BAR_HEIGHT/2
            player_2.score += 1 
            time_initial = time.time()
            ball.reset()

        if ball.x >= player_2.x + BAR_WIDTH:
            player_1.y, player_2.y = HEIGHT/2 - BAR_HEIGHT/2, HEIGHT/2 - BAR_HEIGHT/2
            player_1.score += 1 
            time_initial = time.time()
            ball.reset()

        if elapsed_time <= 3 and ball.y_dir == 0 and ball.x_dir == 0: 
            ball.y_dir = ball.BALL_SPEED * random.randrange(-1, 2, 2)
            ball.x_dir = ball.BALL_SPEED * random.randrange(-1, 2, 2)
            
        if elapsed_time > 3:
            player_1.bar_movement_1()
            ball.ball_movement()
            ball.collision(player_1, player_2)

        if automate:
            player_2.automate(ball)

        elif not automate and elapsed_time > 3:
            player_2.bar_movement_2()
        
        pygame.display.update()
    
    pygame.quit()

start()