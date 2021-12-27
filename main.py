import pygame
from pygame import mixer
import random
import math

pygame.init()
mixer.init()
pygame.font.init()

# CONSTANTS
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = (int)(SCREEN_WIDTH * 0.8)
BG = (105, 105, 105)
BG_IMAGE = pygame.image.load('C:/Users/rijad/Desktop/laser_game/misc/bg_image.jpg')
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60

original_wizard1image = pygame.image.load('C:/Users/rijad/Desktop/laser_game/good/wizard1.png')
original_wizard2image = pygame.image.load('C:/Users/rijad/Desktop/laser_game/good/wizard2.png')
original_zombieimage = pygame.image.load('C:/Users/rijad/Desktop/laser_game/bad/zombie.png')

# MUSIC CONSTANTS
main_menu_music = pygame.mixer.Sound('C:/Users/rijad/Desktop/laser_game/music/main_menu.mp3')
main_menu_music.set_volume(1)
# funny_bit, retro_platforming, castle_of_fear
music = pygame.mixer.Sound('C:/Users/rijad/Desktop/laser_game/music/funny_bit.mp3')
music.set_volume(0.7)
laser_sfx = pygame.mixer.Sound('C:/Users/rijad/Desktop/laser_game/music/lasersfx.wav')
laser_sfx.set_volume(0.5)

# FONT CONSTANTS
font = pygame.font.Font('C:/Users/rijad/AppData/Local/Microsoft/Windows/Fonts/8-bit Arcade In.ttf', 100)

# DISPLAY
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2_laser_game")

# DEFINE PLAYER ACTION VARIBALES
one_moving_left = False
one_moving_right = False
one_moving_up = False
one_moving_down = False

two_moving_left = False
two_moving_right = False
two_moving_up = False
two_moving_down = False


class Character(pygame.sprite.Sprite):
    def __init__(self, number, x, y, scale, speed):
        self.speed = speed
        self.scale = scale
        self.number = number

        image = pygame.image.load(f'C:/Users/rijad/Desktop/laser_game/good/wizard{number}.png').convert_alpha()
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right, moving_up, moving_down):
        # promjena x i y koordinate
        dx = 0
        dy = 0

        if moving_left:
            if self.rect.left > 0:
                dx = -self.speed
        if moving_right:
            if self.rect.right < SCREEN_WIDTH:
                dx = self.speed
        if moving_up:
            if self.rect.top > 0:
                dy = -self.speed
        if moving_down:
            if self.rect.bottom < SCREEN_HEIGHT:
                dy = self.speed

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        if self.number == '1':
            main = (main1.rect.center)
            secondary = (main2.rect.center)
        else:
            main = (main2.rect.center)
            secondary = (main1.rect.center)
        ang_x, ang_y = secondary[0] - main[0], secondary[1] - main[1]
        angle = (180 / math.pi) * - math.atan2(ang_y, ang_x) - 90
        if self.number == '1':
            self.image = pygame.transform.rotozoom(original_wizard1image, int(angle), self.scale)
            screen.blit(self.image, self.rect)
        else:
            self.image = pygame.transform.rotozoom(original_wizard2image, int(angle), self.scale)
            screen.blit(self.image, self.rect)



class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self, zombie_group)
        self.speed = speed
        self.check = 0
        self.num = random.choice(main)
        self.scale = scale

        img = pygame.image.load('C:/Users/rijad/Desktop/laser_game/bad/zombie.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        dx = self.speed
        dy = self.speed

        if self.rect.x > self.num.rect.x:
            self.rect.x += -dx
        else:
            self.rect.x += dx

        if self.rect.y > self.num.rect.y:
            self.rect.y += -dy
        else:
            self.rect.y += dy

        #self.check += 1

        # collision with player
        if self.rect.colliderect(main1) or self.rect.colliderect(main2):
            pygame.display.quit()


    def draw(self):
        if self.num == main1:
            main = (self.rect.center)
            secondary = (main1.rect.center)
        else:
            main = (self.rect.center)
            secondary = (main2.rect.center)
        ang_x, ang_y = secondary[0] - main[0], secondary[1] - main[1]
        angle = (180 / math.pi) * -math.atan2(ang_y, ang_x) - 270
        self.image = pygame.transform.rotozoom(original_zombieimage, int(angle), self.scale)
        screen.blit(self.image, self.rect)


def draw_bg():
    screen.fill(BG)
    screen.blit(BG_IMAGE, (0, 0))

def draw_tutorial():
    wasd_blue = pygame.image.load('C:/Users/rijad/Desktop/laser_game/misc/wasd.png')
    wasd_red = pygame.image.load('C:/Users/rijad/Desktop/laser_game/misc/arrowkeys.png')
    wasd_blue = pygame.transform.scale(wasd_blue, (wasd_blue.get_width() * 0.3, wasd_blue.get_height() * 0.3))
    wasd_red = pygame.transform.scale(wasd_red, (wasd_red.get_width() * 0.3, wasd_red.get_height() * 0.3))
    screen.blit(wasd_blue, (main1.rect.centerx - 55, main1.rect.centery - 100))
    screen.blit(wasd_red, (main2.rect.centerx - 55, main2.rect.centery - 100))

def distance_point_line(pt, l1, l2):
    NV = pygame.math.Vector2(l1[1] - l2[1], l2[0] - l1[0])
    LP = pygame.math.Vector2(l1)  # moze i l2
    P = pygame.math.Vector2(pt)
    return abs(
        NV.normalize().dot(P - LP))  # dot je mnozenje vektora sa skalarom. P-LP je smjer koji main1 ima prema zombie


# GROUPS
zombie_group = pygame.sprite.Group()
shooter_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
tank_group = pygame.sprite.Group()


# ----------------------------------------------------- MAIN ----------------------------------------------------------

clock = pygame.time.Clock()
click = False

# Character(number, x, y, scale, speed)
main1 = Character('1', 400, 400, 1, 3)
main2 = Character('2', 600, 400, 1, 3)
main = [main1, main2]

def game():
    max_zombie_timer = 300
    zombie_timer = 0  # 5 sekundi jer 300/FPS = 5, FPS = 60
    score = 0
    tutorial_timer = 300

    global one_moving_left, one_moving_right, one_moving_up, one_moving_down
    global two_moving_left, two_moving_right, two_moving_up, two_moving_down

    main_menu_music.stop()
    music.play(-1, 0, 0)

    run = True
    while run:
        clock.tick(FPS)
        draw_bg()

        if tutorial_timer > 0:
            draw_tutorial()
        tutorial_timer -= 1

        score_text = font.render(str(score), False, WHITE)
        screen.blit(score_text, (30, 1))

        main1.draw()
        main2.draw()

        main1.move(one_moving_left, one_moving_right, one_moving_up, one_moving_down)
        main2.move(two_moving_left, two_moving_right, two_moving_up, two_moving_down)

        laser = pygame.draw.line(screen, WHITE, (main1.rect.centerx + 12, main1.rect.centery + 10),
                                 (main2.rect.centerx - 25, main2.rect.centery + 10), 6)

        # Zombie(x, y, scale, speed)
        if zombie_timer == max_zombie_timer:
            # za koliko ce enemy biti spawnan van ekrana = 10
            ran = random.randint(1, 4)
            if ran == 1:
                zombie = Zombie((SCREEN_WIDTH + 10), (random.randint(0, SCREEN_HEIGHT)), 0.8, 1)
            if ran == 2:
                zombie = Zombie((random.randint(0, SCREEN_WIDTH)), (-10), 0.8, 1)
            if ran == 3:
                zombie = Zombie((SCREEN_WIDTH - 10), (random.randint(0, SCREEN_HEIGHT)), 0.8, 1)
            if ran == 4:
                zombie = Zombie((random.randint(0, SCREEN_WIDTH)), (SCREEN_HEIGHT + 10), 0.8, 1)
            zombie_group.add(zombie)
            max_zombie_timer -= 10
            zombie_timer = 0
        zombie_timer += 1

        zombie_group.draw(screen)
        for zombie in zombie_group:
            zombie.move()
            zombie.draw()
            if laser.collidepoint(zombie.rect.center) and distance_point_line(zombie.rect.center, main1.rect.center,
                                                                              main2.rect.center) < 10:
                laser_sfx.play(1, 0, 0)
                zombie.kill()
                score += 1

        # quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            # keyboard presses

            if event.type == pygame.KEYDOWN:
                # movement
                if event.key == pygame.K_a:
                    one_moving_left = True
                if event.key == pygame.K_d:
                    one_moving_right = True
                if event.key == pygame.K_w:
                    one_moving_up = True
                if event.key == pygame.K_s:
                    one_moving_down = True

                if event.key == pygame.K_LEFT:
                    two_moving_left = True
                if event.key == pygame.K_RIGHT:
                    two_moving_right = True
                if event.key == pygame.K_UP:
                    two_moving_up = True
                if event.key == pygame.K_DOWN:
                    two_moving_down = True

            if event.type == pygame.KEYUP:
                # -movement
                if event.key == pygame.K_a:
                    one_moving_left = False
                if event.key == pygame.K_d:
                    one_moving_right = False
                if event.key == pygame.K_w:
                    one_moving_up = False
                if event.key == pygame.K_s:
                    one_moving_down = False

                if event.key == pygame.K_LEFT:
                    two_moving_left = False
                if event.key == pygame.K_RIGHT:
                    two_moving_right = False
                if event.key == pygame.K_UP:
                    two_moving_up = False
                if event.key == pygame.K_DOWN:
                    two_moving_down = False

        pygame.display.update()

def main_menu():
    main_menu_music.play(-1, 0, 0)
    button_play = pygame.image.load('C:/Users/rijad/Desktop/laser_game/misc/button_play.png')
    button_play_hover = pygame.image.load('C:/Users/rijad/Desktop/laser_game/misc/button_play_hover.png')
    button_exit = pygame.image.load('C:/Users/rijad/Desktop/laser_game/misc/button_exit.png')
    button_exit_hover = pygame.image.load('C:/Users/rijad/Desktop/laser_game/misc/button_exit_hover.png')
    while True:
        clock.tick(FPS)
        draw_bg()
        global click

        mx, my = pygame.mouse.get_pos()

        logo = pygame.image.load('C:/Users/rijad/Desktop/laser_game/misc/logo.png')
        screen.blit(logo, (100, 200))

        screen.blit(button_play, (100, 400))
        button_play_rect = pygame.Rect(100, 400, 350, 100)
        if button_play_rect.collidepoint((mx, my)):
            screen.blit(button_play_hover, (100, 400))
            if click:
                game()
        screen.blit(button_exit, (550, 400))
        button_exit_rect = pygame.Rect(550, 400, 350, 100)
        if button_exit_rect.collidepoint((mx, my)):
            screen.blit(button_exit_hover, (550, 400))
            if click:
                pygame.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

main_menu()



