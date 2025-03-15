import sys
import os
import random
import pygame

# ---------------------------
# 打包專用：取得正確的資源路徑（用於讀取圖片、音樂等）
def resource_path(relative_path):
    """
    將相對路徑轉為絕對路徑。當程式打包後，資源會存放在 sys._MEIPASS 內。
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# ---------------------------

# ---------------------------
# 記錄檔處理：使用使用者家目錄存放記錄檔，檔名 ".monster_fall_record.txt"
def get_record_path():
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, ".monster_fall_record.txt")

def load_record():
    path = get_record_path()
    if not os.path.exists(path):
        return 0.0  # 如果沒有記錄檔則預設為 0
    try:
        with open(path, 'r') as f:
            return float(f.read())
    except Exception:
        return 0.0

def save_record(record):
    path = get_record_path()
    with open(path, 'w') as f:
        f.write(str(record))
# ---------------------------

FPS = 240

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

WIDTH = 800
HEIGHT = 500
GROUND_HEIGHT = 50

# 初始化 pygame 與混音器、建立視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Fall")
clock = pygame.time.Clock()

# 讀取圖片（使用 resource_path）
player_img = pygame.image.load(resource_path('image/player.png'))
player_img = pygame.transform.scale(player_img, (40, 40))

clock_img = pygame.image.load(resource_path('image/clock.png'))
clock_img = pygame.transform.scale(clock_img, (40, 40))

death_img = pygame.image.load(resource_path('image/death.png'))
death_img = pygame.transform.scale(death_img, (40, 40))

start_btn_img = pygame.image.load(resource_path('image/start_btn.png'))
restart_btn_img = pygame.image.load(resource_path('image/restart_btn.png'))
restart_btn_img = pygame.transform.scale(restart_btn_img, (75, 75))

start_btn_pressed_img = pygame.image.load(resource_path('image/start_btn_pressed.png'))
restart_btn_pressed_img = pygame.image.load(resource_path('image/restart_btn_pressed.png'))
restart_btn_pressed_img = pygame.transform.scale(restart_btn_pressed_img, (75, 75))

score_board_img = pygame.image.load(resource_path('image/score_board.png'))
score_board_img = pygame.transform.scale(score_board_img, (300, 250))

background_img = pygame.image.load(resource_path('image/background.jpg'))
grass_img = pygame.image.load(resource_path('image/grass.jpg'))
grass_img = pygame.transform.scale(grass_img, (1000, 250))

bonus_imgs = [pygame.transform.scale(pygame.image.load(resource_path(f'image/{i}.png')), (35, 35)) for i in range(1, 4)]
monster_imgs = [pygame.image.load(resource_path(f'image/monster{i}.png')) for i in range(1, 11)]

pygame.display.set_icon(player_img)  # 設定視窗左上角 icon

# 載入音量圖示
volume_on_img = pygame.image.load(resource_path('image/volume_on.png'))
volume_on_img = pygame.transform.scale(volume_on_img, (40, 40))
volume_off_img = pygame.image.load(resource_path('image/volume_off.png'))
volume_off_img = pygame.transform.scale(volume_off_img, (40, 40))
volume_rect = volume_on_img.get_rect()
volume_rect.topright = (WIDTH - 20, 20)

# 讀取記錄檔，改用 load_record（存放在使用者家目錄下）
record = load_record()

# 全域音量控制變數
volume_on = True

def update_volume():
    """根據 volume_on 狀態設定各音效音量"""
    if volume_on:
        background_music.set_volume(0.5)
        scream_music.set_volume(0.2)
        power_up_music.set_volume(0.7)
        break_record_music.set_volume(0.15)
    else:
        background_music.set_volume(0)
        scream_music.set_volume(0)
        power_up_music.set_volume(0)
        break_record_music.set_volume(0)

def draw_volume_icon():
    """清除音量圖示區域後，根據狀態繪製對應圖示"""
    screen.blit(background_img, volume_rect, volume_rect)
    if volume_on:
        screen.blit(volume_on_img, volume_rect)
    else:
        screen.blit(volume_off_img, volume_rect)

def draw_text(surf, text, size, color, x, y):
    font = pygame.font.SysFont("Verdana", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def reset_game():
    """重設遊戲狀態"""
    global all_sprites, enemys, numbers, player, ground
    global timer, two_sec, ten_sec, clock_color, record_color, current, new_record
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
    new_record = False

def draw_init():
    """遊戲初始畫面"""
    screen.blit(background_img, (0, 0))
    draw_text(screen, 'Monster Fall', 60, BLACK, WIDTH/2, HEIGHT/4)
    start_btn_rect = start_btn_img.get_rect()
    start_btn_rect.center = (WIDTH/2, HEIGHT/2+30)
    screen.blit(start_btn_img, start_btn_rect)
    draw_text(screen, 'Record: ' + str(record), 20, BLACK, 100, 30)
    draw_volume_icon()
    pygame.display.update()
    
    waiting = True
    global volume_on
    while waiting:
        clock.tick(FPS)
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.MOUSEBUTTONUP and volume_rect.collidepoint(event.pos):
                volume_on = not volume_on
                update_volume()
                draw_volume_icon()
                pygame.display.update()
            if start_btn_rect.collidepoint((x, y)):
                screen.blit(start_btn_pressed_img, start_btn_rect)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    return False
            else:
                screen.blit(start_btn_img, start_btn_rect)
                pygame.display.update()

def draw_end(timer):
    """遊戲結算畫面"""
    score_board_rect = score_board_img.get_rect()
    score_board_rect.center = (WIDTH/2, HEIGHT/2-20)
    screen.blit(score_board_img, score_board_rect)
    
    timer_text = str(round(timer, 2))
    font = pygame.font.SysFont("Verdana", 64)
    if new_record:
        timer_surface = font.render(timer_text, True, RED)
    else:
        timer_surface = font.render(timer_text, True, BLACK)
    timer_rect = timer_surface.get_rect()
    timer_rect.center = (WIDTH/2, 180)
    screen.blit(timer_surface, timer_rect)
    
    restart_btn_rect = restart_btn_img.get_rect()
    restart_btn_rect.center = (WIDTH/2, HEIGHT/2+25)
    screen.blit(restart_btn_img, restart_btn_rect)
    draw_volume_icon()
    pygame.display.update()

    waiting = True
    global volume_on
    while waiting:
        clock.tick(FPS)
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.MOUSEBUTTONUP and volume_rect.collidepoint(event.pos):
                volume_on = not volume_on
                update_volume()
                draw_volume_icon()
                pygame.display.update()
            if restart_btn_rect.collidepoint((x, y)):
                screen.blit(restart_btn_pressed_img, restart_btn_rect)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    return False
            else:
                screen.blit(restart_btn_img, restart_btn_rect)
                pygame.display.update()

def draw_clock(surf, clock_img, timer, color, size):
    """
    在遊戲畫面上方中央顯示秒數與時鐘圖示，
    並在秒數右上角顯示 new record!（若新紀錄）
    ※ 這裡 timer 位置可根據需求調整
    """
    text = str(round(timer, 2))
    font = pygame.font.SysFont("Verdana", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH/2, 50)
    clock_rect = clock_img.get_rect()
    clock_rect.centery = text_rect.centery
    clock_rect.right = text_rect.left - 10
    surf.blit(clock_img, clock_rect)
    surf.blit(text_surface, text_rect)
    if new_record:
        new_record_font = pygame.font.SysFont("Verdana", int(size * 0.4))
        new_record_surface = new_record_font.render("new record!", True, RED)
        new_record_rect = new_record_surface.get_rect()
        new_record_rect.bottomleft = text_rect.topright
        surf.blit(new_record_surface, new_record_rect)

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
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50
        self.speedx = 3
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
        self.rect.top = HEIGHT - GROUND_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = random.randint(25, 45)
        self.image = pygame.transform.scale(random.choice(monster_imgs), (self.radius*2, self.radius*2))
        self.rect = self.image.get_rect()
        left = random.randrange(-500, -100)
        right = random.randrange(WIDTH+100, WIDTH+500)
        self.rect.centerx = random.choice((left, right))
        self.rect.bottom = random.randrange(150, 300)
        if self.rect.right <= 0:
            self.direction = 'right'
            self.speedx = random.uniform(0.75, 1.25)
        elif self.rect.left >= WIDTH:
            self.direction = 'left'
            self.speedx = -random.uniform(0.75, 1.25)
        self.speedy = 0
        self.acceleration_y = 0.02 * (1.1 ** (ten_sec - 1))

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.speedy += self.acceleration_y
        if self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.speedy *= -1

class Number(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 15
        self.image = random.choice(bonus_imgs)
        self.number = bonus_imgs.index(self.image) + 1
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(50, WIDTH - 50)
        self.rect.centery = -100
        self.speedy = 0
        self.acceleration_y = 0.02

    def update(self):
        self.rect.y += self.speedy
        self.speedy += self.acceleration_y
        if self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.speedy = 0

# 遊戲音效（使用 resource_path 讀取）
background_music = pygame.mixer.Sound(resource_path("music/background.mp3"))
background_music.set_volume(0.5)
background_music.play(-1)
scream_music = pygame.mixer.Sound(resource_path("music/scream.mp3"))
scream_music.set_volume(0.2)
power_up_music = pygame.mixer.Sound(resource_path("music/power_up.mp3"))
power_up_music.set_volume(0.7)
break_record_music = pygame.mixer.Sound(resource_path("music/break_record.mp3"))
break_record_music.set_volume(0.15)
update_volume()

pygame.time.set_timer(pygame.USEREVENT, 100)

running = True
show_init = True
show_end = False

# new_record 旗標，記錄是否破了新紀錄
new_record = False

while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        reset_game()

    if show_end:
        close = draw_end(timer)
        if close:
            break
        show_end = False
        reset_game()

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP and volume_rect.collidepoint(event.pos):
            volume_on = not volume_on
            update_volume()
        elif event.type == pygame.USEREVENT:
            timer += 0.1

    if timer > two_sec * 2 and timer < 10:
        two_sec += 1
        new_enemy()

    if timer > ten_sec * 10:
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

    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, enemys, False, pygame.sprite.collide_circle)
    if hits:
        show_end = True
        player.image = death_img
        break_record_music.stop()
        power_up_music.stop()
        scream_music.play()
        if new_record:
            record = round(timer, 1)
            save_record(record)
    
    hits = pygame.sprite.spritecollide(player, numbers, True, pygame.sprite.collide_circle)
    if hits:
        clock_color = RED
        for hit in hits:
            power_up_music.play()
            timer += hit.number
        current = timer
    if timer - current > 2:
        clock_color = BLACK

    if round(timer, 1) >= record and not show_end and not new_record:
        new_record = True
        record_color = RED
        break_record_music.play()

    screen.fill(WHITE)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_clock(screen, clock_img, timer, clock_color, 30)
    if new_record:
        draw_text(screen, 'Record: ' + str(round(timer, 1)), 20, record_color, 100, 30)
    else:
        draw_text(screen, 'Record: ' + str(record), 20, record_color, 100, 30)
    draw_volume_icon()
    pygame.display.update()

pygame.quit()
