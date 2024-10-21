import pygame, random,sys
from pygame.locals import *

# all colours
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

play_again_button = None
quit_button = None
BULLET_IMAGE = pygame.transform.scale(pygame.image.load("assets/bullet_pic.png"),(10,15))

WIDTH, HEIGHT = 700, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
lane_positions = [x for x in range(100, 501, 50)]
ATTACK_LINE_Y = 500

# bullet imports
speed = 5
BULLET_SPEED = 10
BARRICATE_HIT = pygame.USEREVENT + 2
ZOMBIE_HIT = pygame.USEREVENT + 1
BARRICATE_HEALTH = 500

pygame.font.init()
BARRICATE_HEALTH_FONT = pygame.font.SysFont('Arial', 10)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

MAN_WIDTH, MAN_HEIGHT = 50, 50
man_image_raw1 = pygame.transform.rotate(
    pygame.image.load("assets/max (2).png"), 180)

man_image1 = pygame.transform.scale(man_image_raw1, (MAN_WIDTH, MAN_HEIGHT))

small_enemie1_raw = pygame.transform.scale(pygame.image.load("assets/small_zombie1.png"), (50, 50))
small_enemie2_raw = pygame.transform.scale(pygame.image.load("assets/small_zombie2.png"), (50, 50))
small_enemie3_raw = pygame.transform.scale(pygame.image.load("assets/small_zombie3.png"), (50, 50))
small_enemie4_raw = pygame.transform.scale(pygame.image.load("assets/small_zombie4.png"), (50, 50))

medium_enemy1_raw = pygame.transform.scale(pygame.image.load("assets/medium_zombie1.png"), (50, 50))
medium_enemy2_raw = pygame.transform.scale(pygame.image.load("assets/medium_zombie2.png"), (50, 50))

# list of enemies
small_zombies_list = [small_enemie1_raw,small_enemie2_raw,small_enemie3_raw,small_enemie4_raw]
medium_zombies_list = [medium_enemy1_raw,medium_enemy2_raw]
large_zombies_list = []

enemies = []

ROAD = (100, 0, 500, HEIGHT)
MARKER_WIDTH, MARKER_HEIGHT = 5, 25

def ROAD_SETUP():
    win.fill(GREEN)
    global ROAD
    LEFT_EDGE_MERKER = (95, 0, MARKER_WIDTH, HEIGHT)
    RIGHT_EDGE_MERKER = (595, 0, MARKER_WIDTH, HEIGHT)
    pygame.draw.rect(win, YELLOW, LEFT_EDGE_MERKER)
    pygame.draw.rect(win, YELLOW, RIGHT_EDGE_MERKER)
    # adding all game stats here
    BARRICATE_HEALTH_TEXT = BARRICATE_HEALTH_FONT.render("HEALTH: " + str(BARRICATE_HEALTH), 1, RED)

    win.blit(BARRICATE_HEALTH_TEXT, (10, 10))  # Adjusted the placement of the text

def lane_markers():
    for y in range(MARKER_HEIGHT * -2, HEIGHT, MARKER_HEIGHT * 2):
        pygame.draw.rect(win, WHITE, (100 + 45, y, MARKER_WIDTH, MARKER_HEIGHT))
        pygame.draw.rect(win, WHITE, (150 + 45, y, MARKER_WIDTH, MARKER_HEIGHT))
        pygame.draw.rect(win, WHITE, (200 + 45, y, MARKER_WIDTH, MARKER_HEIGHT))
        pygame.draw.rect(win, WHITE, (250 + 45, y, MARKER_WIDTH, MARKER_HEIGHT))
        pygame.draw.rect(win, WHITE, (300 + 45, y, MARKER_WIDTH, MARKER_HEIGHT))
        pygame.draw.rect(win, WHITE, (350 + 45, y, MARKER_WIDTH, MARKER_HEIGHT))
        pygame.draw.rect(win, WHITE, (400 + 45, y, MARKER_WIDTH, MARKER_HEIGHT))
        pygame.draw.rect(win, WHITE, (450 + 45, y, MARKER_WIDTH, MARKER_HEIGHT))
        pygame.draw.rect(win, WHITE, (500 + 45, y, MARKER_WIDTH, MARKER_HEIGHT))
        # total divisions=10
    barricade_image = pygame.transform.scale(pygame.image.load("assets/barricate.png"), (50, 50))
    barricade = pygame.Rect(0, 500, barricade_image.get_width(), barricade_image.get_height())
    global lane_positions,BARRICATE_HEALTH

    if BARRICATE_HEALTH > 0:
        for x in lane_positions:
            win.blit(barricade_image, (x, 550 ))
            win.blit(barricade_image, (x+25, 550 ))
            win.blit(barricade_image, (x+50, 550 ))
    
def lanes():
    lanes = []
    start = 150
    difference = 50
    end = 551
    for lane in range(start, end, difference):
        lanes.append(lane)
    return lanes

class Bullet:
    def __init__(self, x, y, image):
        self.rect = pygame.Rect(x, y, 5, 20)
        self.image = image
# enemies sequal
# Define classes for enemies
class Enemy:
    def __init__(self, image, x, speed, health, damage):
        self.x = x
        self.y = 0
        self.image = image
        self.speed = speed
        self.health = health
        self.bullets = speed
        self.damage = damage
        self.ZOMBIE_BULLETS = []
        # Create a rect attribute for collision detection
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 0)  # Set the initial position
        self.can_fire = False  # Add a flag to determine if the enemy can fire
        # self.fire_cooldown = 0 # Cooldown for firing bullets

    def update(self):

        # Check if the enemy can fire (reached 400+ y-coordinate)
        if self.y >= 500 and self.health > 0 and BARRICATE_HEALTH > 0:
            self.y = 0
            self.can_fire = True
        else:
            self.y += self.speed
            self.rect.topleft = (self.x, self.y)

        if BARRICATE_HEALTH <= 0:
            self.can_fire = False

        if self.can_fire:
            self.fire_bullet()

        for enemy in enemies:
            win.blit(enemy.image, (enemy.x, enemy.y))

    def fire_bullet(self):

        if len(self.ZOMBIE_BULLETS) <= self.bullets:
            # Create a bullet at the bottom of player 1
            bullet = pygame.Rect(self.rect.x + self.rect.width // 2, self.rect.y, 5, 20)
            self.ZOMBIE_BULLETS.append(bullet)

        global BARRICATE_HEALTH

        # Update the position of each bullet
        for bullet in self.ZOMBIE_BULLETS:
            bullet.y += self.speed  # Move the DOWNWARDS upwards

            if bullet.y >= 500:
                if bullet in self.ZOMBIE_BULLETS:
                    self.ZOMBIE_BULLETS.remove(bullet)
                    BARRICATE_HEALTH -= self.damage

        # Add logic to create and fire bullets
        # Remove bullets that reach a certain y-coordinate
        self.ZOMBIE_BULLETS = [bullet for bullet in self.ZOMBIE_BULLETS if bullet.y < 500]

# summoning of enemies sequal
def summon_enemy_small():
    if random.random() < 0.02:
        random_image = random.choice(small_zombies_list)
        enemy_image = Enemy(random_image, random.choice(lane_positions), 2, 3, 2)
        enemies.append(enemy_image)

def summon_enemy_medium():
    if random.random() < 0.002:
        random_image = random.choice(medium_zombies_list)
        enemy_image = Enemy(random_image, random.choice(lane_positions), 1, 3, 1)
        enemies.append(enemy_image)

def summon_enemy_large():
    if random.random() < 0.0002:
        random_image = random.choice(large_zombies_list)
        enemy_image = Enemy(random_image,random.choice(lane_positions), 0.5, 10,5)
        enemies.append(enemy_image)

def update_enemies():
    if enemy.y >= 500 and BARRICATE_HEALTH > 0:
        Enemy.can_fire = True
        enemy.y = 0
    elif enemy.y < 500:
        for enemy in enemies:
            enemy.y += enemy.speed
            if enemy.y > HEIGHT:
                enemies.remove(enemy)

class Human:
    def __init__(self, image, x, health, max_bullets, damage):
        self.x = x
        self.y = 0
        self.health = health
        self.image = image
        self.max_bullets = max_bullets
        self.damage = damage
        self.MAN_BULLETS = []
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 0)
        self.can_fire = False
        # self.fire_cooldown = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 600)  # Set the initial position
        self.can_fire = False  # Add a flag to determine if the enemy can fire
        # self.fire_cooldown = 0 # Cooldown for firing bullets

    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
        # Draw the player on the window

    def firing(self, key_pressed):
        if key_pressed[K_RCTRL]:
            if len(self.MAN_BULLETS) <= self.max_bullets:
                # Create a bullet at the bottom of the player
                bullet = Bullet(self.rect.x + self.rect.width // 2, self.rect.y, BULLET_IMAGE)
                self.MAN_BULLETS.append(bullet)

    def handle_bullets(self, enemies):
        for bullet in self.MAN_BULLETS:
            win.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
            bullet.rect.y -= BULLET_SPEED  # Move the bullet upwards
            if bullet.rect.y < 0:
                if bullet in self.MAN_BULLETS:
                    self.MAN_BULLETS.remove(bullet)

            for enemy in enemies:
                if enemy.rect.colliderect(bullet):
                    enemies.remove(enemy)
                    if bullet in self.MAN_BULLETS:
                        self.MAN_BULLETS.remove(bullet)

    def move(self, key_pressed):
        # person1
        if key_pressed[pygame.K_LEFT] and self.rect.x >= 150:  # left
            self.x -= 50
        if key_pressed[pygame.K_RIGHT] and self.rect.x <= 500:  # right
            self.x += 50

        # Update the rect position based on the new x
        self.rect.topleft = (self.x, self.rect.y)
        # Implement movement logic here

player1 = Human(man_image1, 300, 10, 20, 1)

def end_screen():
    global play_again_button, quit_button  # Declare the buttons as global

    end_screen_font = pygame.font.Font(None, 60)
    text = end_screen_font.render("YOU DIED", True, BLACK)
    win.fill(RED)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

    # Create "Play Again" button
    play_again_button = pygame.Rect(WIDTH // 2 - 100, 2 * HEIGHT // 3, 220, 50)  # Centered and adjusted button size
    pygame.draw.rect(win, GREEN, play_again_button)
    play_again_text = end_screen_font.render("Play Again", True, BLACK)
    win.blit(play_again_text, (play_again_button.x + (play_again_button.width - play_again_text.get_width()) // 2, play_again_button.y + 15))  # Center-aligned text

    # Create "Quit" button
    quit_button = pygame.Rect(WIDTH // 2 - 100, 2 * HEIGHT // 3 + 60, 220, 50)  # Centered and adjusted button position and size
    pygame.draw.rect(win, GREEN, quit_button)
    quit_text = end_screen_font.render("Quit", True, BLACK)
    win.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2, quit_button.y + 15))  # Center-aligned text

    pygame.display.update()

    return play_again_button, quit_button

def survival_game_main():
    pygame.init()
    pygame.display.set_caption("ZOMBIE SURVIVAL GAME")
    global BARRICATE_HEALTH
    key_pressed = pygame.key.get_pressed()
    FPS = 40
    # set the FPS of the game at which it runs
    clock = pygame.time.Clock()
    pygame.display.update()
    run = True
    game_over = False  # Add a flag to track if the game is over
    end_screen_displayed = False  # Add a flag to track if the end screen is displayed

    while run:
        clock.tick(FPS)

        if not game_over:
            ROAD_SETUP()
            pygame.draw.rect(win, GRAY, ROAD)
            lane_markers()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if not end_screen_displayed:  # Check if the end screen is not displayed
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        m_x, m_y = pygame.mouse.get_pos()
                        print(m_x, m_y)

                    key_pressed = pygame.key.get_pressed()
                    player1.move(key_pressed)

                if BARRICATE_HEALTH <= 0:
                    game_over = True  # Set the game over flag
                    end_screen_displayed = True  # Set the end screen displayed flag

            if not game_over:
                summon_enemy_small()
                for enemy in enemies:
                    enemy.update()

                summon_enemy_medium()
                for enemy in enemies:
                    enemy.update()

                player1.firing(key_pressed)
                player1.handle_bullets(enemies)
                player1.draw()
                pygame.display.update()
            else:
                # Display the end screen
                play_again_button, quit_button = end_screen()  # Display the end screen and get the buttons

        if game_over and end_screen_displayed:
            # Handle the buttons only when the game is over and the end screen is displayed
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    if play_again_button.collidepoint(m_x, m_y):
                        game_over = False
                        end_screen_displayed = False
                        BARRICATE_HEALTH = 500  # Reset barricade health
                        enemies.clear()  # Clear the list of enemies
                        player1.x = 300  # Reset player's position
                        player1.health = 10  # Reset player's health
                    elif quit_button.collidepoint(m_x, m_y):
                        pygame.quit()
                        sys.exit()

    pygame.quit()

# survival_game_main()

