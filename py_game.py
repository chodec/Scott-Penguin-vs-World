import pygame, math, random

pygame.init()

BLACK = (0, 0, 0)
CRIMSON = (220, 20, 60)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 2 
TILE_SIZE = 32
SCALE_FACTOR = 1 
SCALE_PLAYER = 2
FPS = 60
SHOOT_COOLDOWN = 1000  
ENEMY_SPAWN_COOLDOWN = 2500
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Scott Penguin vs World')

sprite_sheet = pygame.image.load('tileset.png').convert_alpha()

player_sprite_sheet = pygame.image.load('penguin.png').convert_alpha()

def get_tile(sheet, col, row, width, height):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (col * width, row * height, width, height))
    image = pygame.transform.scale(image, (width * SCALE_FACTOR, height * SCALE_FACTOR))
    return image

def get_projectile_sprite(sheet, col, row, width, height):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (col * width, row * height, width, height))
    return image

grass_tile = get_tile(sprite_sheet, 0, 15, TILE_SIZE, TILE_SIZE)
road_tile_1 = get_tile(sprite_sheet, 7, 15, TILE_SIZE, TILE_SIZE)
road_tile_2 = get_tile(sprite_sheet, 9, 15, TILE_SIZE, TILE_SIZE)
road_tile_3 = get_tile(sprite_sheet, 10, 15, TILE_SIZE, TILE_SIZE)
road_tile_4 = get_tile(sprite_sheet, 12, 15, TILE_SIZE, TILE_SIZE)
road_tile_5 = get_tile(sprite_sheet, 13, 15, TILE_SIZE, TILE_SIZE)

projectile_up = get_projectile_sprite(sprite_sheet, 44, 10, TILE_SIZE, TILE_SIZE)
projectile_right = get_projectile_sprite(sprite_sheet, 46, 10, TILE_SIZE, TILE_SIZE)
projectile_down = get_projectile_sprite(sprite_sheet, 48, 10, TILE_SIZE, TILE_SIZE)
projectile_left = get_projectile_sprite(sprite_sheet, 50, 10, TILE_SIZE, TILE_SIZE)

map_layout = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 2, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 3, 1, 4, 0, 5, 1, 2, 5, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 1, 4, 0, 0, 0, 5, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 2, 0, 0],
    [1, 1, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 1, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

enemy_sprite = get_tile(sprite_sheet, 0, 3, TILE_SIZE, TILE_SIZE)

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 5
        self.direction = direction
        if direction == "up":
            self.image = projectile_up
        elif direction == "right":
            self.image = projectile_right
        elif direction == "down":
            self.image = projectile_down
        elif direction == "left":
            self.image = projectile_left

    def update(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Player:
    def __init__(self, x, y, sprite_sheet):
        self.x = x
        self.y = y
        self.sprite_sheet = sprite_sheet
        self.current_frame = 0
        self.animation_speed = 0.1
        self.frame_counter = 0
        self.direction = "right"
        self.health = 100
        self.right_sprites = [self.get_sprite(i, 0) for i in range(7)]
        self.left_sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.right_sprites]
        self.up_sprites = [self.get_sprite(i, 1) for i in range(7)]
        self.current_sprites = self.right_sprites
        self.bullets = []
        self.last_shot_time = pygame.time.get_ticks()

    def get_sprite(self, frame, row):
        image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (frame * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        image = pygame.transform.scale(image, (TILE_SIZE * SCALE_PLAYER, TILE_SIZE * SCALE_PLAYER))
        return image

    def update(self, keys):
        if keys[pygame.K_w]:
            self.y -= PLAYER_SPEED
            self.direction = "up"
        elif keys[pygame.K_s]:
            self.y += PLAYER_SPEED
            self.direction = "down"
        elif keys[pygame.K_a]:
            self.x -= PLAYER_SPEED
            self.direction = "left"
        elif keys[pygame.K_d]:
            self.x += PLAYER_SPEED
            self.direction = "right"

        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            self.frame_counter += self.animation_speed
            if self.frame_counter >= len(self.right_sprites):
                self.frame_counter = 0
            self.current_frame = int(self.frame_counter)
        
        if self.direction == "right" or self.direction == "down":
            self.current_sprites = self.right_sprites
        elif self.direction == "left":
            self.current_sprites = self.left_sprites
        elif self.direction == "up":
            self.current_sprites = self.up_sprites

        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        sprite = self.current_sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_x = SCREEN_WIDTH - HEALTH_BAR_WIDTH - 10
        bar_y = SCREEN_HEIGHT - HEALTH_BAR_HEIGHT - 10
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT), 2)
        fill_width = (self.health / 100) * (HEALTH_BAR_WIDTH - 4)
        pygame.draw.rect(screen, CRIMSON, (bar_x + 2, bar_y + 2, fill_width, HEALTH_BAR_HEIGHT - 4))

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= SHOOT_COOLDOWN:
            bullet_x = self.x + TILE_SIZE // 2 * SCALE_PLAYER
            bullet_y = self.y + TILE_SIZE // 2 * SCALE_PLAYER
            new_bullet = Projectile(bullet_x, bullet_y, self.direction)
            self.bullets.append(new_bullet)
            self.last_shot_time = current_time

class Enemy:
    def __init__(self, x, y, health, damage, speed):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.speed = speed
        self.image = enemy_sprite

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist

        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Scott Penguin vs World')
        self.clock = pygame.time.Clock()
        self.sprite_sheet = pygame.image.load('penguin.png').convert_alpha()
        self.player = Player(400, 300, self.sprite_sheet)
        self.enemies = []
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.running = True

    def draw_map(self):
        for row_index, row in enumerate(map_layout):
            for col_index, tile in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if tile == 0:
                    self.screen.blit(grass_tile, (x, y))
                elif tile == 1:
                    self.screen.blit(road_tile_1, (x, y))
                elif tile == 2:
                    self.screen.blit(road_tile_2, (x, y))
                elif tile == 3:
                    self.screen.blit(road_tile_3, (x, y))
                elif tile == 4:
                    self.screen.blit(road_tile_4, (x, y))
                elif tile == 5:
                    self.screen.blit(road_tile_5, (x, y))

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time >= ENEMY_SPAWN_COOLDOWN:
            x = random.randint(0, SCREEN_WIDTH - TILE_SIZE)
            y = random.randint(0, SCREEN_HEIGHT - TILE_SIZE)
            new_enemy = Enemy(x, y, health=50, damage=10, speed=1)
            self.enemies.append(new_enemy)
            self.last_enemy_spawn_time = current_time

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.shoot()

            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.spawn_enemy()
            for enemy in self.enemies:
                enemy.update(self.player)

            self.screen.fill(BLACK)
            self.draw_map()
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
