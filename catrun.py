import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Cat Run")

game_font = pygame.font.Font("CatRun/assets/PressStart2P-Regular.ttf", 24)


# Classes


class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1


class Catosaur(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/frame00.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/frame01.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/frame02.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/frame03.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/frame04.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/frame05.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/frame06.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/frame07.png"), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/duckframe00.png"), (100, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/duckframe01.png"), (100, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/duckframe02.png"), (100, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/duckframe03.png"), (100, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/duckframe04.png"), (100, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/duckframe05.png"), (100, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/duckframe06.png"), (100, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"assets/duckframe07.png"), (100, 60)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 50
        self.gravity = 4.5
        self.ducking = False

    def jump(self):
        jump_sfx.play()
        if self.rect.centery >= 360:
            while self.rect.centery - self.velocity > 40:
                self.rect.centery -= 1

    def duck(self):
        self.ducking = True
        self.rect.centery = 380

    def unduck(self):
        self.ducking = False
        self.rect.centery = 360

    def apply_gravity(self):
        if self.rect.centery <= 360:
            self.rect.centery += self.gravity

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.08
        if self.current_image >= 8:
            self.current_image = 0

        if self.ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.image = self.running_sprites[int(self.current_image)]


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"assets/cacti/cactus{i}.png"), (70, 80))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([280, 295, 350])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Ptero1.png"), (84, 62)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Ptero2.png"), (84, 62)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]


# Variables


game_speed = 6
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

# Surfaces

ground = pygame.image.load("assets/ground.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center=(640, 300))
cloud = pygame.image.load("assets/cloud.png")
cloud = pygame.transform.scale(cloud, (200, 80))

# Groups

cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
catosaur_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()

# Objects
cat = Catosaur(50, 360)
catosaur_group.add(cat)

# Sounds
death_sfx = pygame.mixer.Sound("assets/sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("assets/sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("assets/sfx/jump.mp3")

# Events
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)


# Functions


def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 6
    cloud_group.empty()
    obstacle_group.empty()


while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        cat.duck()
    else:
        if cat.ducking:
            cat.unduck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 300)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                cat.jump()
                if game_over:
                    game_over = False
                    game_speed = 6
                    player_score = 0

    screen.fill("white")

    # Collisions
    if pygame.sprite.spritecollide(catosaur_group.sprite, obstacle_group, False):
        game_over = True
        death_sfx.play()
    if game_over:
        end_game()

    if not game_over:
        game_speed += 0.0020
        if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
            points_sfx.play()

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            obstacle_random = random.randint(1, 50)
            if obstacle_random in range(1, 7):
                new_obstacle = Cactus(1260, 340)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(7, 10):
                new_obstacle = Ptero()
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False

        player_score += 0.1
        player_score_surface = game_font.render(
            str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (1150, 10))

        cloud_group.update()
        cloud_group.draw(screen)

        ptero_group.update()
        ptero_group.draw(screen)

        catosaur_group.update()
        catosaur_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        ground_x -= game_speed

        screen.blit(ground, (ground_x, 360))
        screen.blit(ground, (ground_x + 1280, 360))

        if ground_x <= -1280:
            ground_x = 0

    clock.tick(120)
    pygame.display.update()
