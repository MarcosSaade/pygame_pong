import pygame
import sys
import random
import statistics
import time


class LineLeft():
    def __init__(self):
        self.width = 10
        self.length = 130
        self.pos_y = 230
        self.speed = 0

    def draw(self):
        line_rect = pygame.Rect(20, self.pos_y, self.width, self.length)
        pygame.draw.rect(screen, (255, 255, 255), line_rect)

    def move(self):
        if self.pos_y >= 450:
            self.pos_y = 450
        elif self.pos_y <= 20:
            self.pos_y = 20

        self.pos_y += self.speed

        return self.pos_y, self.pos_y + self.length


class LineRight():
    def __init__(self):
        self.width = 10
        self.length = 130
        self.pos_y = 230
        self.speed = 0

    def draw(self):
        line_rect = pygame.Rect(770, self.pos_y, self.width, self.length)
        pygame.draw.rect(screen, (255, 255, 255), line_rect)

    def move(self):
        if main.ai:
            self.pos_y = main.ball.y -20

        if self.pos_y >= 450:
            self.pos_y = 450
        elif self.pos_y <= 20:
            self.pos_y = 20

        self.pos_y += self.speed

        return self.pos_y, self.pos_y + self.length


class Ball():
    def __init__(self):
        self.x = 400
        self.y = 300
        self.speed_x = 10
        self.speed_y = 0
        self.direction = "left"
        self.line_left = LineLeft()
        self.line_right = LineRight()

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 5)

    def move(self):
        if self.y >= 580:
            if main.hard_mode:
                self.speed_y = -2
            else:
                self.speed_y = -1
        elif self.y <= 15:
            if main.hard_mode:
                self.speed_y = 2
            else:
                self.speed_y = 1

        if self.x == 20:
            if main.collision_left():
                self.direction = "right"
            else:
                main.player_two_score += 1
                main.game_over = True

            pos_line_l = statistics.mean([main.line_left.move()[0], main.line_left.move()[1]]) + 5

            if pos_line_l > self.y:
                self.speed_y -= 1
            elif pos_line_l < self.y:
                self.speed_y += 1

        elif self.x in [770, 760]:
            if main.collision_right():
                self.direction = "left"
            else:
                if main.hard_mode:
                    main.player_one_score += 1
                    main.game_over = True
                if not main.hard_mode:
                    print("1")
                    main.player_one_score += 0.5
                    main.game_over = True

            pos_line_r = statistics.mean([main.line_right.move()[0], main.line_right.move()[1]]) + 5

            if pos_line_r > self.y:
                self.speed_y -= 1
            elif pos_line_r < self.y:
                self.speed_y += 1

        if main.hard_mode:
            if self.direction == "left":
                self.speed_x = -20
            elif self.direction == "right":
                self.speed_x = 20
        else:
            if self.direction == "left":
                self.speed_x = -10
            elif self.direction == "right":
                self.speed_x = 10

        self.x += self.speed_x
        self.y += self.speed_y


class Main():
    def __init__(self):
        self.line_left = LineLeft()
        self.line_right = LineRight()
        self.ball = Ball()
        self.game_over = False

        self.player_one_score = 0
        self.player_two_score = 0

        self.menu = False
        self.options = False

        self.color = (0, 0, 0)

        self.hard_mode = False
        self.ai = False

    def update(self):
        if self.menu:
            self.menu_func()
        elif self.options:
            self.options_func()

        if not self.menu and not self.options:
            self.draw_board()

            self.line_left.draw()
            self.line_left.move()

            self.line_right.draw()
            self.line_right.move()

            self.ball.draw()
            self.ball.move()

            self.ball.y += self.ball.speed_y

            self.reset = False

            if self.game_over:
                self.game_over_fun()
            if self.reset:
                self.reset_func()

    def draw_board(self):
        middle_line = pygame.Rect(398, 10, 2, 578)
        top_line = pygame.Rect(0, 10, 800, 2)
        bottom_line = pygame.Rect(0, 588, 800, 2)

        pygame.draw.rect(screen, (255, 255, 255), middle_line)
        pygame.draw.rect(screen, (255, 255, 255), top_line)
        pygame.draw.rect(screen, (255, 255, 255), bottom_line)

    def collision_left(self):
        return self.ball.y in range(self.line_left.move()[0], self.line_left.move()[1])

    def collision_right(self):
        return int(self.ball.y) in range(self.line_right.move()[0], self.line_right.move()[1])

    def game_over_fun(self):
        font = pygame.font.Font("Andromeda-Bold.otf", 64)
        game_over_font = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_font, (210, 20))

        font_small = pygame.font.Font("Andromeda-Bold.otf", 28)

        options_font_p = font_small.render("To play again press P", True, (255, 255, 255))
        screen.blit(options_font_p, (100, 110))

        options_font_e = font_small.render("To return to menu press M", True, (255, 255, 255))
        screen.blit(options_font_e, (420, 110))

        font_medium = pygame.font.Font("Andromeda-Bold.otf", 42)

        player_one = font_medium.render(str(int(self.player_one_score)), True, (255, 255, 255))
        screen.blit(player_one, (360, 500))

        player_two = font_medium.render(str(self.player_two_score), True, (255, 255, 255))
        screen.blit(player_two, (425, 500))

    def reset_func(self):
        self.ball.y = 300
        self.ball.x = 400
        self.ball.speed_x = 10
        self.ball.speed_y = 0
        self.ball.direction = "left"

        self.line_left.pos_y = 230
        self.line_right.pos_y = 230

        self.reset = False

    def menu_func(self):
        font_menu = pygame.font.Font("Andromeda-Bold.otf", 100)
        f_menu = font_menu.render("PONG", True, (255, 255, 255))
        screen.blit(f_menu, (270, 20))

        font_menu_small = pygame.font.Font("Andromeda-Bold.otf", 24)
        font_menu_smaller = pygame.font.Font("Andromeda-Bold.otf", 18)

        if round(time.time()) % 10 in [1, 3, 5, 7, 9]:
            color = (255, 255, 255)
            f_menu_small = font_menu_small.render("Press P to play", True, color)
        else:
            color = self.color
            f_menu_small = font_menu_small.render("Press P to play", True, color)

        f_options = font_menu_smaller.render("Press O for options", True, (64, 64, 64))

        screen.blit(f_menu_small, (325, 500))
        screen.blit(f_options, (630, 560))

        self.player_one_score = 0
        self.player_two_score = 0

    def options_func(self):
        font_options_small = pygame.font.Font("Andromeda-Bold.otf", 24)
        f_options_blue = font_options_small.render("Press B for blue background", True, (0, 0, 128))
        f_options_green = font_options_small.render("Press G for green background", True, (0, 128, 0))
        f_options_black = font_options_small.render("Press K for black background", True, (128, 128, 128))

        hard = font_options_small.render("Difficulty: Hard", True, (128, 0, 0))
        easy = font_options_small.render("Difficulty: Easy", True, (100, 100, 192))
        f_options_hard = font_options_small.render("Press H for hard mode", True, (128, 0, 0))
        f_options_easy = font_options_small.render("Press E for easy mode", True, (100, 100, 192))

        single_player = font_options_small.render("Mode: Single player", True, (128, 128, 0))
        two_players = font_options_small.render("Mode: Two players", True, (0, 128, 128))
        f_options_one_p = font_options_small.render("Press 1 for Single player mode", True, (128, 128, 0))
        f_options_two_p = font_options_small.render("Press 2 for two player mode", True, (0, 128, 128))

        f_options_menu = font_options_small.render("Press M to go back to main menu", True, (255, 255, 255))

        # Color
        screen.blit(f_options_blue, (10, 30))
        screen.blit(f_options_green, (10, 70))
        screen.blit(f_options_black, (10, 110))

        # Difficulty
        if self.hard_mode:
            screen.blit(hard, (10, 210))
        else:
            screen.blit(easy, (10, 210))

        screen.blit(f_options_hard, (10, 250))
        screen.blit(f_options_easy, (10, 280))

        # AI
        if self.ai:
            screen.blit(single_player, (10, 380))
        else:
            screen.blit(two_players, (10, 380))

        screen.blit(f_options_one_p, (10, 420))
        screen.blit(f_options_two_p, (10, 450))

        # Menu
        screen.blit(f_options_menu, (10, 550))


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
main = Main()
main.menu = True
main.menu_func()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if not main.ai:
                if event.key == pygame.K_UP:
                    main.line_right.speed = -8
                if event.key == pygame.K_DOWN:
                    main.line_right.speed = 8
            if event.key == pygame.K_w:
                main.line_left.speed = -8
            if event.key == pygame.K_s:
                main.line_left.speed = 8
            if main.game_over == True:
                if event.key == pygame.K_p:
                    main.reset = True
                    main.reset_func()
                    main.game_over = False
                if event.key == pygame.K_m:
                    main.menu = True
            if main.menu:
                if event.key == pygame.K_p:
                    main.menu = False
                if event.key == pygame.K_o:
                    main.menu = False
                    main.options = True
            if main.options:
                if event.key == pygame.K_b:
                    main.color = (30, 50, 128)
                if event.key == pygame.K_g:
                    main.color = (50, 192, 50)
                if event.key == pygame.K_k:
                    main.color = (0, 0, 0)
                if event.key == pygame.K_h:
                    main.hard_mode = True
                if event.key == pygame.K_e:
                    main.hard_mode = False
                if event.key == pygame.K_1:
                    main.ai = True
                if event.key == pygame.K_2:
                    main.ai = False
                if event.key == pygame.K_m:
                    main.options = False
                    main.menu = True

        if event.type == pygame.KEYUP:
            if not main.ai:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    main.line_right.speed = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                main.line_left.speed = 0

    screen.fill(main.color)
    main.update()
    pygame.display.update()
    clock.tick(60)