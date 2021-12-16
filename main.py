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
BG_IMAGE = pygame.image.load('C:/Users/rijad/Desktop/laser_game/bg_image.jpg')
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60

original_wizard1image = pygame.image.load('C:/Users/rijad/Desktop/laser_game/good/wizard1.png')
original_wizard2image = pygame.image.load('C:/Users/rijad/Desktop/laser_game/good/wizard2.png')
original_zombieimage = pygame.image.load('C:/Users/rijad/Desktop/laser_game/bad/zombie.png')

# MUSIC CONSTANTS
main_menu_music = pygame.mixer.Sound('C:/Users/rijad/Desktop/laser_game/music/main_menu.mp3')
main_menu_music.set_volume(0.01)
# main_menu_music.play(-1, 0, 0)
# funny_bit, retro_platforming, castle_of_fear
music = pygame.mixer.Sound('C:/Users/rijad/Desktop/laser_game/music/castle_of_fear.mp3')
music.set_volume(0.008)
music.play(-1, 0, 0)
laser_sfx = pygame.mixer.Sound('C:/Users/rijad/Desktop/laser_game/music/lasersfx.wav')

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
            self.image = pygame.transform.rotozoom(original_wizard1image, int(angle), 3)
            screen.blit(self.image, self.rect)
        else:
            self.image = pygame.transform.rotozoom(original_wizard2image, int(angle), 3)
            screen.blit(self.image, self.rect)



class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self, zombie_group)
        self.speed = speed
        self.check = 0
        self.num = random.choice(main)

        img = pygame.image.load('C:/Users/rijad/Desktop/laser_game/bad/zombie.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        dx = self.speed
        dy = self.speed

        # chase random main character
        """if self.check == 0:
            self.num = random.choice(main)"""

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
            main = (zombie.rect.center)
            secondary = (main1.rect.center)
        else:
            main = (zombie.rect.center)
            secondary = (main2.rect.center)
        ang_x, ang_y = secondary[0] - main[0], secondary[1] - main[1]
        angle = (180 / math.pi) * -math.atan2(ang_y, ang_x) - 270
        self.image = pygame.transform.rotozoom(original_zombieimage, int(angle), 2.5)
        screen.blit(self.image, self.rect)

class Shooter(pygame.sprite.Sprite):
    def __init(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self, zombie_group)
        self.speed = speed

        img = pygame.image.load('C:/Users/rijad/Desktop/laser_game/bad/2.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        dx = self.speed
        dy = self.speed


def draw_bg():
    screen.fill(BG)
    screen.blit(BG_IMAGE, (0, 0))


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

max_zombie_timer = 300
zombie_timer = 0  # 5 sekundi jer 300/FPS = 5, FPS = 60
max_shooter_timer = 480
shooter_timer = 0
score = 0

# MAIN

clock = pygame.time.Clock()

# Character(number, x, y, scale, speed)
# Zombie(x, y, scale, speed)
main1 = Character('1', 400, 400, 2.5, 3)
main2 = Character('2', 600, 400, 2.5, 3)
main = [main1, main2]

run = True
while run:
    draw_bg()
    clock.tick(FPS)

    score_text = font.render(str(score), False, WHITE)
    screen.blit(score_text, (30, 1))

    main1.draw()
    main2.draw()

    main1.move(one_moving_left, one_moving_right, one_moving_up, one_moving_down)
    main2.move(two_moving_left, two_moving_right, two_moving_up, two_moving_down)

    laser = pygame.draw.line(screen, WHITE, (main1.rect.centerx + 12, main1.rect.centery + 10), (main2.rect.centerx + 5, main2.rect.centery + 10), 6)

    # zombie
    if zombie_timer == max_zombie_timer:
        # za koliko ce enemy biti spawnan van ekrana = 10
        ran = random.randint(1, 4)
        if ran == 1:
            zombie = Zombie((SCREEN_WIDTH + 10), (random.randint(0, SCREEN_HEIGHT)), 3, 1)
        if ran == 2:
            zombie = Zombie((random.randint(0, SCREEN_WIDTH)), (-10), 3, 1)
        if ran == 3:
            zombie = Zombie((SCREEN_WIDTH - 10), (random.randint(0, SCREEN_HEIGHT)), 3, 1)
        if ran == 4:
            zombie = Zombie((random.randint(0, SCREEN_WIDTH)), (SCREEN_HEIGHT + 10), 3, 1)
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

    #shooter
    """shooter_timer == max_shooter_timer:
        ran = random.randint(1, 4)
        if ran == 1:
            shooter = Shooter((SCREEN_WIDTH + 10), (random.randint(0, SCREEN_HEIGHT)), 1, 1)
        if ran == 2:
            shooter = Shooter((random.randint(0, SCREEN_WIDTH)), (-10), 1, 1)
        if ran == 3:
            shooter = Shooter((SCREEN_WIDTH - 10), (random.randint(0, SCREEN_HEIGHT)), 1, 1)
        if ran == 4:
            shooter = Shooter((random.randint(0, SCREEN_WIDTH)), (SCREEN_HEIGHT + 10), 1, 1)

        shooter_group.add(shooter)
        max_shooter_timer -= 5
        zombie_timer = 0
    shooter_timer += 1

    shooter_group.draw(screen)
    for shooter in shooter_group:
        shooter.move()
        if laser.collidepoint(zombie.rect.center) and distance_point_line(shooter.rect.center, main1.rect.center, main2.rect.center) < 5:
            shooter.kill()
            score += 1"""

    # quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
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