import pygame, math, random

pygame.init()
pygame.mixer.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CRIMSON = (220, 20, 60)
LIGHT_GREEN = (124, 252, 0)
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
XP_BAR_WIDTH = 200
XP_BAR_HEIGHT = 20
FONT_SIZE = 24

menu_music = pygame.mixer.Sound('ameno.mp3')
game_music = pygame.mixer.Sound('GloriousMorning.mp3')
shoot_sound = pygame.mixer.Sound('bow.mp3')
enemy_death_sound = pygame.mixer.Sound('death_mob.mp3')
player_death_sound = pygame.mixer.Sound('player_death.mp3')
level_up_sound = pygame.mixer.Sound('dominating.mp3')

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

def get_item_tile(sheet, col, row, width, height):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (col * width, row * height, width, height))
    return image

def get_animation_frames(sheet, start_col, end_col, row, width, height):
    frames = []
    for col in range(start_col, end_col + 1):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (col * width, row * height, width, height))
        frames.append(image)
    return frames

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

exp_tile = get_item_tile(sprite_sheet, 1, 10, TILE_SIZE, TILE_SIZE)

animation_frames = get_animation_frames(sprite_sheet, 13, 20, 12, TILE_SIZE, TILE_SIZE)
animation_death_frames = get_animation_frames(sprite_sheet, 25, 32, 7, TILE_SIZE, TILE_SIZE)

enemy_sprite = get_tile(sprite_sheet, 0, 3, TILE_SIZE, TILE_SIZE)

background_tile = get_tile(sprite_sheet, 22, 13, TILE_SIZE, TILE_SIZE)

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

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
        self.animation_frames = animation_frames
        self.current_frame = 0
        self.animation_speed = 0.1
        self.frame_counter = 0
        self.background_tile = background_tile
        pygame.mixer.Sound.play(menu_music, loops=-1)

    def stop_music(self):
        pygame.mixer.Sound.stop(menu_music)

    def draw(self):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                self.screen.blit(self.background_tile, (x, y))

        font = pygame.font.SysFont(None, 48)
        play_text = font.render('Start', True, WHITE)

        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render('Scott Penguin vs World', True, CRIMSON)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2 + 15, 200))
        self.screen.blit(title_text, title_rect)

        for y in range(self.play_button.y, self.play_button.y + self.play_button.height, TILE_SIZE):
            for x in range(self.play_button.x, self.play_button.x + self.play_button.width, TILE_SIZE):
                self.screen.blit(self.background_tile, (x, y))

        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.animation_frames):
            self.frame_counter = 0
        self.current_frame = int(self.frame_counter)

        frame_image = self.animation_frames[self.current_frame]
        self.screen.blit(frame_image, (self.play_button.x + 10, self.play_button.y + 5))
        self.screen.blit(frame_image, (self.play_button.x + 150, self.play_button.y + 5))
        self.screen.blit(play_text, (self.play_button.x + 60, self.play_button.y + 10))
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                return True
        return False

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 5
        self.direction = direction
        self.alive = True 
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
        if self.alive:
            screen.blit(self.image, (self.x, self.y))

    def destroy(self):
        self.alive = False

class Item:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

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
        self.xp = 0
        self.level = 1
        self.projectile_count = 1
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

    def check_level_up(self):
        if self.xp >= 100:
            self.level += 1
            self.xp = 0
            self.projectile_count += 1
            pygame.mixer.Sound.play(level_up_sound) 

    def collect_item(self, item):
        self.xp += 10
        self.check_level_up()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            pygame.mixer.Sound.play(player_death_sound)

    def draw(self, screen):
        sprite = self.current_sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen)
        self.draw_health_bar(screen)
        self.draw_xp_bar(screen)
        self.draw_level(screen)

    def draw_health_bar(self, screen):
        bar_x = SCREEN_WIDTH - HEALTH_BAR_WIDTH - 10
        bar_y = SCREEN_HEIGHT - HEALTH_BAR_HEIGHT - 10
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT), 2)
        fill_width = (self.health / 100) * (HEALTH_BAR_WIDTH - 4)
        pygame.draw.rect(screen, CRIMSON, (bar_x + 2, bar_y + 2, fill_width, HEALTH_BAR_HEIGHT - 4))
        font = pygame.font.SysFont(None, 24)
        hp_text = font.render('HP', True, BLACK)
        screen.blit(hp_text, (bar_x - 30, bar_y))
    
    def draw_xp_bar(self, screen):
        bar_x = 40
        bar_y = SCREEN_HEIGHT - XP_BAR_HEIGHT - 10
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, XP_BAR_WIDTH, XP_BAR_HEIGHT), 2)
        fill_width = (self.xp / 100) * (XP_BAR_WIDTH - 4)
        pygame.draw.rect(screen, LIGHT_GREEN, (bar_x + 2, bar_y + 2, fill_width, XP_BAR_HEIGHT - 4))
        font = pygame.font.SysFont(None, 24)
        xp_text = font.render('XP', True, BLACK)
        screen.blit(xp_text, (bar_x - 30, bar_y))

    def draw_level(self, screen):
        font = pygame.font.SysFont(None, 24)
        level_text = font.render(f'Level {self.level}', True, BLACK)
        text_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(level_text, text_rect)

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= SHOOT_COOLDOWN:
            bullets = []
            for i in range(self.projectile_count):
                bullet_x = self.x + TILE_SIZE // 2 * SCALE_PLAYER
                bullet_y = self.y + TILE_SIZE // 2 * SCALE_PLAYER
                new_bullet = Projectile(bullet_x + i * 10, bullet_y + i * 10, self.direction)
                bullets.append(new_bullet)
                self.bullets.append(new_bullet)
            self.last_shot_time = current_time
            pygame.mixer.Sound.play(shoot_sound)
            return bullets
        return None

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

    def drop_item(self):
        return Item(self.x, self.y, exp_tile)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Scott Penguin vs World')
        self.clock = pygame.time.Clock()
        self.sprite_sheet = pygame.image.load('penguin.png').convert_alpha()
        self.player = Player(400, 300, self.sprite_sheet)
        self.enemies = []
        self.items = []
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.running = True
        self.menu = Menu(self.screen)
        self.state = 'menu'
        self.death_animation_frames = animation_death_frames
        self.current_frame = 0
        self.animation_speed = 0.1
        self.frame_counter = 0

    
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
    
    def check_collisions(self):
        for item in list(self.items):
            if self.player.x < item.x + TILE_SIZE and self.player.x + TILE_SIZE > item.x and \
               self.player.y < item.y + TILE_SIZE and self.player.y + TILE_SIZE > item.y:
                self.player.collect_item(item)
                self.items.remove(item)

        for enemy in list(self.enemies):
            if self.player.x < enemy.x + TILE_SIZE and self.player.x + TILE_SIZE > enemy.x and \
               self.player.y < enemy.y + TILE_SIZE and self.player.y + TILE_SIZE > enemy.y:
                self.player.take_damage(0.3)
                if self.player.health <= 0:
                    self.state = 'death'

    def draw_death_screen(self):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                self.screen.blit(self.menu.background_tile, (x, y))

        font = pygame.font.SysFont(None, 72)
        death_text = font.render('Game Over', True, CRIMSON)
        retry_text = font.render('Respawn', True, BLACK)
        retry_text_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.screen.blit(death_text, (SCREEN_WIDTH // 2 - death_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))

        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.death_animation_frames):
            self.frame_counter = 0
        self.current_frame = int(self.frame_counter)

        frame_image = self.death_animation_frames[self.current_frame]
        self.screen.blit(frame_image, (retry_text_rect.left - TILE_SIZE, retry_text_rect.centery - TILE_SIZE // 2))
        self.screen.blit(frame_image, (retry_text_rect.right, retry_text_rect.centery - TILE_SIZE // 2))
        self.screen.blit(frame_image, (retry_text_rect.centerx - TILE_SIZE // 2, retry_text_rect.top - TILE_SIZE))
        self.screen.blit(frame_image, (retry_text_rect.centerx - TILE_SIZE // 2, retry_text_rect.bottom))

        self.screen.blit(retry_text, retry_text_rect)
        pygame.display.flip()

        return retry_text_rect

    def run(self):
        self.projectiles = []

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.state == 'menu':
                    if self.menu.handle_event(event):
                        self.state = 'game'
                        self.menu.stop_music()
                        pygame.mixer.Sound.stop(menu_music)
                        pygame.mixer.Sound.play(game_music, loops=-1)
                elif self.state == 'game':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            bullets = self.player.shoot()
                            if bullets:
                                self.projectiles.extend(bullets)
                elif self.state == 'death':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        retry_button = self.draw_death_screen()
                        if retry_button.collidepoint(event.pos):
                            self.__init__()
                            pygame.mixer.Sound.stop(game_music)
                            pygame.mixer.Sound.play(menu_music, loops=-1)

            if self.state == 'menu':
                self.menu.draw()
            elif self.state == 'game':
                keys = pygame.key.get_pressed()
                self.player.update(keys)
                self.spawn_enemy()

                for projectile in list(self.projectiles):
                    projectile.update()
                    if not projectile.alive:
                        self.projectiles.remove(projectile)

                for enemy in list(self.enemies):
                    enemy.update(self.player)
                    for projectile in list(self.projectiles):
                        dist = math.hypot(enemy.x - projectile.x, enemy.y - projectile.y)
                        if dist < TILE_SIZE:
                            self.enemies.remove(enemy)
                            item = enemy.drop_item()
                            self.items.append(item)
                            projectile.destroy()
                            pygame.mixer.Sound.play(enemy_death_sound)
                            break

                self.check_collisions()

                self.screen.fill(BLACK)
                self.draw_map()
                self.player.draw(self.screen)
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                for item in self.items:
                    item.draw(self.screen)
                for projectile in self.projectiles:
                    projectile.draw(self.screen)
                pygame.display.flip()

            elif self.state == 'death':
                retry_button = self.draw_death_screen()

            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
