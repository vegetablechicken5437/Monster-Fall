import random
import pygame

FPS = 240   

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 180, 100)
RED = (255, 0, 0)

WIDTH = 800
HEIGHT = 500
GROUND_HEIGHT = 50

# 初始化pygame、創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("Monster Fall")
clock = pygame.time.Clock()

# 讀取圖片
player_img = pygame.image.load('image/player.png')
player_img = pygame.transform.scale(player_img, (40, 40))
clock_img = pygame.image.load('image/clock.png')
clock_img = pygame.transform.scale(clock_img, (40, 40))
death_img = pygame.image.load('image/death.png')
death_img = pygame.transform.scale(death_img, (40, 40))
start_btn_img = pygame.image.load('image/start_btn.png')
restart_btn_img = pygame.image.load('image/restart_btn.png')
restart_btn_img = pygame.transform.scale(restart_btn_img, (75, 75))
start_btn_pressed_img = pygame.image.load('image/start_btn_pressed.png')
restart_btn_pressed_img = pygame.image.load('image/restart_btn_pressed.png')
restart_btn_pressed_img = pygame.transform.scale(restart_btn_pressed_img, (75, 75))
score_board_img = pygame.image.load('image/score_board.png')
score_board_img = pygame.transform.scale(score_board_img, (300, 250))
background_img = pygame.image.load('image/background.jpg')
grass_img = pygame.image.load('image/grass.jpg')
grass_img = pygame.transform.scale(grass_img, (1000, 250))

bonus_imgs = [pygame.transform.scale(pygame.image.load(f'image/{i}.png'), (35, 35)) for i in range(1, 4)]
monster_imgs = [pygame.image.load(f'image/monster{i}.png') for i in range(1, 11)]

pygame.display.set_icon(player_img)     # 設定左上角icon

# 分數紀錄檔案
with open('record.txt', 'r') as f:
    record = float(f.read())

def draw_text(surf, text, size, color, x, y):
    font = pygame.font.SysFont("Verdana", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, 'Monster Fall', 60, BLACK, WIDTH/2, HEIGHT/4) 
    start_btn_rect = start_btn_img.get_rect()
    start_btn_rect.centerx, start_btn_rect.centery = WIDTH/2, HEIGHT/2+30
    screen.blit(start_btn_img, start_btn_rect)
    draw_text(screen, 'Record: '+str(record), 20, BLACK, 100, 30)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True         
            if x >= start_btn_rect.left and x <= start_btn_rect.right and y >= start_btn_rect.top and y <= start_btn_rect.bottom:
                screen.blit(start_btn_pressed_img, start_btn_rect)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    return False
            else:
                screen.blit(start_btn_img, start_btn_rect)
                pygame.display.update()
        
def draw_end(timer):
    score_board_img_rect = score_board_img.get_rect()
    score_board_img_rect.centerx, score_board_img_rect.centery = WIDTH/2, HEIGHT/2-20
    screen.blit(score_board_img, score_board_img_rect)

    draw_text(screen, str(round(timer, 2)), 64, BLACK, WIDTH/2, 145)
    restart_btn_rect = restart_btn_img.get_rect()
    restart_btn_rect.centerx, restart_btn_rect.centery = WIDTH/2, HEIGHT/2+25
    screen.blit(restart_btn_img, restart_btn_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(FPS)
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True               
            if x >= restart_btn_rect.left and x <= restart_btn_rect.right and y >= restart_btn_rect.top and y <= restart_btn_rect.bottom:
                screen.blit(restart_btn_pressed_img, restart_btn_rect)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    return False
            else:
                screen.blit(restart_btn_img, restart_btn_rect)
                pygame.display.update()
     
def draw_clock(surf, clock, timer, color, size):
    draw_text(surf, str(round(timer, 2)), size, color, 730, 50)
    surf.blit(clock, (645, 50))

def new_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemys.add(enemy)

def new_number():
    number = Number()
    all_sprites.add(number)
    numbers.add(number)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.radius = 15
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50
        self.speedx = 3
        # self.speedx = 4
        self.direction = 'right'

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
            if self.direction == 'left':
                self.direction = 'right'
                self.image = pygame.transform.flip(self.image, True, False)
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
            if self.direction == 'right':
                self.direction = 'left'
                self.image = pygame.transform.flip(self.image, True, False)

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = grass_img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.top = HEIGHT-GROUND_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = random.randint(25, 45)
        self.image = pygame.transform.scale(random.choice(monster_imgs), (self.radius*2, self.radius*2))
        self.rect = self.image.get_rect()

        left, right = random.randrange(-500, -100), random.randrange(WIDTH+100, WIDTH+500)
        self.rect.centerx = random.choice((left, right))
        self.rect.bottom = random.randrange(150, 300)

        if self.rect.right <= 0:
            self.direction = 'right'
            self.speedx = random.uniform(0.75, 1.25)
        elif self.rect.left >= WIDTH:
            self.direction = 'left'           
            self.speedx = -random.uniform(0.75, 1.25)
        
        self.speedy = 0
        self.acceleration_y = 0.02 * (1.1**(ten_sec-1))

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.speedy += self.acceleration_y
        if self.rect.bottom >= HEIGHT-GROUND_HEIGHT:
            self.speedy *= -1

class Number(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 15
        self.image = random.choice(bonus_imgs)
        self.number = bonus_imgs.index(self.image) + 1
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.centerx = random.randrange(50, WIDTH-50)
        self.rect.centery = -100
        
        self.speedy = 0
        self.acceleration_y = 0.02

    def update(self):
        self.rect.y += self.speedy
        self.speedy += self.acceleration_y
        if self.rect.bottom >= HEIGHT-GROUND_HEIGHT:
            self.speedy = 0

# 遊戲音效
background_music = pygame.mixer.Sound("music/background.mp3")
background_music.set_volume(0.5)
background_music.play(-1)
scream_music = pygame.mixer.Sound("music/scream.mp3")
scream_music.set_volume(0.2)
power_up_music = pygame.mixer.Sound("music/power_up.mp3")
power_up_music.set_volume(0.7)
break_record_music = pygame.mixer.Sound("music/break_record.mp3")
break_record_music.set_volume(0.15)

# 設定計時器
pygame.time.set_timer(pygame.USEREVENT, 100) 

running = True
show_init = True
show_end = False

# 遊戲迴圈
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False

        all_sprites = pygame.sprite.Group()
        enemys = pygame.sprite.Group()
        numbers = pygame.sprite.Group()
        
        player = Player()
        all_sprites.add(player)
        ground = Ground()
        all_sprites.add(ground)

        timer = 0
        two_sec = 0
        ten_sec = 1
        clock_color = BLACK
        record_color = BLACK
        current = 0
        break_record = False

    if show_end:
        close = draw_end(timer)
        if close:
            break
        show_end = False

        all_sprites = pygame.sprite.Group()
        enemys = pygame.sprite.Group()
        numbers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        ground = Ground()
        all_sprites.add(ground)

        timer = 0
        two_sec = 0
        ten_sec = 1
        clock_color = BLACK
        record_color = BLACK
        current = 0
        break_record = False

    clock.tick(FPS)

    # get inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            timer += 0.1

    if timer > two_sec*2 and timer < 10:
        two_sec += 1
        new_enemy()

    if timer > ten_sec*10:
        ten_sec += 1
        new_enemy()
        new_number()

    for enemy in enemys:
        if enemy.direction == 'right' and enemy.rect.left > WIDTH:
            enemy.kill()
            new_enemy()
        elif enemy.direction == 'left' and enemy.rect.right < 0:
            enemy.kill()
            new_enemy()

    # update game
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, enemys, False, pygame.sprite.collide_circle)
    if hits:
        show_end = True
        player.image = death_img
        break_record_music.stop()
        power_up_music.stop()
        scream_music.play()
        if break_record:
            break_record = False
            record = round(timer, 1)
            f = open('record.txt', 'w')
            f.write(str(record))
            f.close()
    
    hits = pygame.sprite.spritecollide(player, numbers, True, pygame.sprite.collide_circle)
    if hits:
        clock_color = RED
        for hit in hits:
            power_up_music.play()
            timer += hit.number
        current = timer
    if timer-current > 2:
        clock_color = BLACK

    if round(timer, 1) >= record and not show_end and not break_record:
        power_up_music.stop()
        break_record = True
        record_color = RED
        break_record_music.play()


    # display on screen
    screen.fill(WHITE)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_clock(screen, clock_img, timer, clock_color, 30)
    if break_record:
        draw_text(screen, 'Record: '+str(round(timer, 1)), 20, record_color, 100, 30)
    else:
        draw_text(screen, 'Record: '+str(record), 20, record_color, 100, 30)
    pygame.display.update()

pygame.quit()