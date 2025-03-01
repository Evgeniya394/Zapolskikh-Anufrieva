import pygame
import os
import sys
import math
import numpy as np

from random import randint, choices, choice


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image


def draw_experience_bar():
    pygame.draw.rect(screen, (150, 150, 150), (0, 0, 1920, 40))
    pygame.draw.rect(screen, (14, 110, 251), (0, 0, 1920 *
                                              (player.experience / (30 * player.level ** 1.08 + 45)), 40))

def main_menu():
    text_start = myfont_128.render("START", True, (255, 15, 55))
    start_x = 350
    start_y = 200

    text_start_back = myfont_128.render("START", True, (248, 210, 51))
    start_back_x = 345
    start_back_y = 195

    text_exit = myfont_128.render("EXIT", True, (255, 15, 55))
    exit_x = 350
    exit_y = 350

    text_exit_back = myfont_128.render("EXIT", True, (248, 210, 51))
    exit_back_x = 345
    exit_back_y = 345

    background_image = load_image("title_screen.png")
    background_image = pygame.transform.scale(background_image, (1920, 1080))
    menu_running = True

    while menu_running:
        screen.blit(background_image, (0, 0))
        screen.blit(text_start_back, (start_back_x, start_back_y))
        screen.blit(text_exit_back, (exit_back_x, exit_back_y))
        screen.blit(text_start_back, (start_back_x + 10, start_back_y))
        screen.blit(text_exit_back, (exit_back_x + 10, exit_back_y))
        screen.blit(text_start, (start_x, start_y))
        screen.blit(text_exit, (exit_x, exit_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                rect = pygame.Rect(start_x, start_y, text_start.get_width(), text_start.get_height())
                if pygame.Rect.collidepoint(rect, pos):
                    menu_running = False
                rect = pygame.Rect(exit_x, exit_y, text_exit.get_width(), text_start.get_height())
                if pygame.Rect.collidepoint(rect, pos):
                    menu_running = False
                    exit(0)
        pygame.display.flip()


def pause():
    pause_menu_picture = load_image('pause_screen.png')
    pause_menu_picture = pygame.transform.scale(pause_menu_picture, size)
    screen.blit(pause_menu_picture, (0, 0))

    continue_text = myfont_128.render("CONTINUE", True, (255, 245, 245))
    exit_text = myfont_128.render("EXIT", True, (255, 245, 245))

    screen.blit(continue_text, (600, 420))
    screen.blit(exit_text, (770, 570))

    paused = True
    while paused:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                paused = False
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                rect = pygame.Rect(600, 420, continue_text.get_width(), continue_text.get_height())
                if pygame.Rect.collidepoint(rect, pos):
                    paused = False
                    player.pause_timer = 3000
                rect = pygame.Rect(770, 570, exit_text.get_width(), continue_text.get_height())
                if pygame.Rect.collidepoint(rect, pos):
                    paused = False
                    sys.exit(0)
            if keys[pygame.K_ESCAPE] or keys[pygame.K_p] or keys[pygame.K_SPACE]:
                paused = False
                player.pause_timer = 3000

        pygame.display.flip()


def level_up():
    player.stats["upgrades gotten"] = player.stats["upgrades gotten"] + 1
    level_up_sound = pygame.mixer.Sound("data/sounds/level_up.wav")
    pygame.mixer.find_channel(True).play(level_up_sound)

    text_level_up = myfont_64.render("НОВЫЙ УРОВЕНЬ!", True, (0, 50, 30))
    level_up_x = 700
    level_up_y = 180

    try:
        upgrades = choices(list(filter(lambda x: x[1] < x[2], player.upgrades)), k=3)
    except IndexError:
        return

    rects = [((520, 330), myfont_48.render(upgrades[0][0], True, (0, 50, 30)),
              pygame.Rect(500, 300, 900, 100), (215, 195, 115),
              myfont_48.render(upgrades[0][3], True, (0, 50, 30)), (1250, 330)),
             ((520, 500), myfont_48.render(upgrades[1][0], True, (0, 50, 30)),
              pygame.Rect(500, 470, 900, 100), (215, 195, 115),
              myfont_48.render(upgrades[1][3], True, (0, 50, 30)), (1250, 500)),
             ((520, 670), myfont_48.render(upgrades[2][0], True, (0, 50, 30)),
              pygame.Rect(500, 640, 900, 100), (215, 195, 115),
              myfont_48.render(upgrades[2][3], True, (0, 50, 30)), (1250, 670))]

    window = pygame.Rect(450, 170, 1000, 800)
    window_color = (235, 213, 133)

    leveling_up = True

    while leveling_up:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    for rect in enumerate(rects):
                        if pygame.Rect.collidepoint(rect[1][2], pos):
                            player.upgrades[player.upgrades.index(upgrades[rect[0]])][1] += 1
                            leveling_up = False

        pygame.draw.rect(screen, window_color, window, 1000, 15)
        for rect in rects:
            pygame.draw.rect(screen, rect[3], rect[2], 50, 5)
            screen.blit(rect[1], rect[0])
            screen.blit(rect[4], rect[5])
        screen.blit(text_level_up, (level_up_x, level_up_y))
        pygame.display.flip()
    sword.scale()


def game_over():
    game_over_sound = pygame.mixer.Sound("data/sounds/game_over.wav")
    pygame.mixer.find_channel(True).play(game_over_sound)
    time = 0
    game_over = True
    surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)

    global running
    running = False
    while game_over:
        time += clock.get_time()
        if time > 2000:
            game_over = False
        surface.fill((255, 0, 0, 2))
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    with open("data/results.txt", "r") as file:
        lines = file.readlines()
        if len(lines) > 7:
            lines.pop(-1)
        lines.insert(0, ";".join(list(map(str, player.stats.values()))))
        lines = list(map(lambda x: x.rstrip("\n"), lines))
        lines = "\n ".join(lines)
        lines = lines.split(" ")
    print(lines)
    open("data/results.txt", "w").writelines(lines)
    result_menu()


def result_menu():
    results_menu_picture = load_image('results_menu.png')
    results_menu_picture = pygame.transform.scale(results_menu_picture, size)
    screen.blit(results_menu_picture, (0, 0))

    game_over_text = myfont_128.render("GAME OVER!", True, (255, 245, 245))
    stats_text = myfont_64.render("STATISTICS:", True, (255, 245, 245))
    exit_text = myfont_128.render("EXIT?", True, (255, 245, 245))

    game_over_dest = (50, 20)
    stats_text_dest = (750, 170)
    exit_text_dest = (1000, 900)

    list1 = ["run N"]
    list1.extend(player.stats.keys())
    headers_texts = [myfont_32.render(key, True, (255, 245, 245))
                      for key in list1]
    headers_dests = [(100, 300 + 65 * key) for key in range(len(list1))]

    with open("data/results.txt", "r") as file:
        stats = list(map(lambda x: x.rstrip("\n").split(";"), file.readlines()))
        for a in enumerate(stats):
            for x in enumerate(a[1]):
                if x[0] > 0:
                    stats[a[0]][x[0]] = str(math.floor(float(x[1])))

    stats_texts = [[myfont_32.render(a, True, (255, 245, 245)) for a in stat] for stat in stats]
    stats_dests = [[(550 + 160 * stat, 365 + 65 * a) for a in range(len(stats[0]))] for stat in range(len(stats))]

    screen.blit(game_over_text, game_over_dest)
    screen.blit(stats_text, stats_text_dest)
    screen.blit(exit_text, exit_text_dest)

    for text in enumerate(headers_texts):
        screen.blit(text[1], headers_dests[text[0]])

    for stat in enumerate(stats_texts):
        screen.blit(myfont_32.render(str(stat[0] + 1), True, (255, 245, 245)),
                    (stats_dests[stat[0]][0][0], stats_dests[stat[0]][0][1] - 65))
        for text in enumerate(stat[1]):
            screen.blit(text[1], stats_dests[stat[0]][text[0]])
    result = True
    while result:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                result = False
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                rect = pygame.Rect(*exit_text_dest, exit_text.get_width(), exit_text.get_height())
                if pygame.Rect.collidepoint(rect, pos):
                    result = False
                    sys.exit(0)

        pygame.display.flip()

class EnemySpawner:
    def __init__(self):
        self.time = 0
        self.wave_time = 0
        self.timer = 0
        self.wave_enemies = 20
        self.wave_interval = 15000
        self.wave_counter = 1
        self.enemies = [#path                       x    y    w   h   hp dmg speed
                        ("enemies/serp_carpet.png", None, None, 80, 100, 20, 10, 90, 15),
                        ("enemies/serp_triangle.png", None, None, 98, 82, 10, 4, 150, 8),
                        ("enemies/c_curve.png", None, None, 63, 63, 50, 10, 70, 30),
                        ("enemies/dragon_curve.png", None, None, 55, 76, 150, 25, 60, 95),
                        ("enemies/apollo_gasket.png", None, None, 97, 97, 300, 50, 50, 300)]

    def spawn_enemy(self):
        x, y, d = randint(-100, 2000), randint(-100, 1200), randint(0, 3)
        if d == 0:
            y = -200
        elif d == 1:
            y = 1300
        elif d == 2:
            x = -200
        elif d == 3:
            x = 2000

        en = choice(self.enemies)
        enemy = Enemy(en[0], x, y, en[3], en[4], en[5], en[6], en[7], en[8])
        enemies.add(enemy)

    def update(self):
        self.timer += clock.get_time()
        self.wave_time += clock.get_time()
        if self.timer >= self.wave_interval / self.wave_enemies:
            self.spawn_enemy()
            self.timer = 0
            self.wave_enemies -= 1
        if self.wave_time >= self.wave_interval:
            self.wave_enemies = 5 + 3 * self.wave_counter + 1.3 ** self.wave_counter
            self.wave_counter += 1
            player.stats["wave reached"] = player.stats["wave reached"] + 1
            self.wave_time = 0


class Map(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.tile_probabilities = [0.225, 0.225, 0.225, 0.225, 0.05, 0.02, 0.03]
        self.tile_ids = [1, 2, 3, 4, 5, 6, 7]
        self.matrix = np.array([[np.random.choice(self.tile_ids, p=self.tile_probabilities)
                                 for _ in range(10)] for _ in range(10)])

        self.rect = pygame.Rect(500, 500, 640, 640)
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)

        tile_size = (64, 64)
        self.grass_1 = load_image('tiles/grass_1.png', 1)
        self.grass_1 = pygame.transform.scale(self.grass_1, tile_size)
        self.grass_2 = load_image('tiles/grass_2.png', 1)
        self.grass_2 = pygame.transform.scale(self.grass_2, tile_size)
        self.grass_3 = load_image('tiles/grass_3.png', 1)
        self.grass_3 = pygame.transform.scale(self.grass_3, tile_size)
        self.grass_4 = load_image('tiles/grass_4.png', 1)
        self.grass_4 = pygame.transform.scale(self.grass_4, tile_size)
        self.bush = load_image('tiles/bush.png', 1)
        self.bush = pygame.transform.scale(self.bush, tile_size)
        self.stomp = load_image('tiles/stomp.png', 1)
        self.stomp = pygame.transform.scale(self.stomp, tile_size)
        self.tree_1 = load_image('tiles/tree_1.png', 1)
        self.tree_1 = pygame.transform.scale(self.tree_1, tile_size)
        self.tree_2 = load_image('tiles/tree_2.png', 1)
        self.tree_2 = pygame.transform.scale(self.tree_2, tile_size)
        self.tree_1_top = load_image('tiles/tree_1_top.png', -1)
        self.tree_1_top = pygame.transform.scale(self.tree_1_top, tile_size)
        self.tree_2_top = load_image('tiles/tree_2_top.png', -1)
        self.tree_2_top = pygame.transform.scale(self.tree_2_top, tile_size)

    def update(self, v_x, v_y):
        tile_x, tile_y = 0, 0
        if self.rect.x + 960 > player.rect.x + player.rect.width // 2:
            self.matrix = np.insert(self.matrix, 0, [0 for _ in range(np.shape(self.matrix)[0])], axis=1)
            for i in range(np.shape(self.matrix)[0]):
                if 1080 > self.rect.y + i * 64 > 0:
                    self.matrix[i][0] = np.random.choice(self.tile_ids, p=self.tile_probabilities)
            self.pos.x -= 64
        elif self.rect.x + self.rect.width - 960 < player.rect.x + player.rect.width // 2:
            self.matrix = np.insert(self.matrix, np.shape(self.matrix)[1],
                                    [0 for _ in range(np.shape(self.matrix)[0])], axis=1)
            for i in range(np.shape(self.matrix)[0]):
                if 1080 > self.rect.y + i * 64 > 0:
                    self.matrix[i][np.shape(self.matrix)[1] - 1] = (
                        np.random.choice(self.tile_ids, p=self.tile_probabilities))
            self.rect.width += 64
        if self.rect.y + 640 > player.rect.y + player.rect.height // 2:
            self.matrix = np.insert(self.matrix, 0, [0 for _ in range(np.shape(self.matrix)[1])], axis=0)
            for i in range(np.shape(self.matrix)[1]):
                if 1920 > self.rect.x + i * 64 > 0:
                    self.matrix[0][i] = np.random.choice(self.tile_ids, p=self.tile_probabilities)
            self.pos.y -= 64
        elif self.rect.y + self.rect.height - 540 < player.rect.y + player.rect.height // 2:
            self.matrix = np.insert(self.matrix, np.shape(self.matrix)[0],
                                    [0 for _ in range(np.shape(self.matrix)[1])], axis=0)
            for i in range(np.shape(self.matrix)[1]):
                if 1920 > self.rect.x + i * 64 > 0:
                    self.matrix[np.shape(self.matrix)[0] - 1][i] = (
                        np.random.choice(self.tile_ids, p=self.tile_probabilities))
            self.rect.height += 64
        if any(filter(lambda x: x == 7, self.matrix[0])):
            self.matrix = np.insert(self.matrix, 0, [np.random.choice(self.tile_ids, p=self.tile_probabilities)
                                                     for _ in range(len(self.matrix[0]))], axis=0)
            self.pos.y -= 64

        while self.rect.x + tile_x * 64 < -64:
            tile_x += 1
        while self.rect.y + tile_y * 64 < -64:
            tile_y += 1

        for row in enumerate(self.matrix[tile_y:tile_y + 19]):
            for item in enumerate(row[1][tile_x:tile_x + 31]):
                if item[1] == 8 and len(self.matrix) > row[0] + tile_y + 1 and self.matrix[row[0] + tile_y + 1][
                        item[0] + tile_x] != 7:
                    self.matrix[row[0] + tile_y][item[0] + tile_x] = np.random.choice(self.tile_ids,
                                                                                      p=self.tile_probabilities)
                if item[1] == 7 and self.matrix[row[0] + tile_y - 1][item[0] + tile_x] != 8:
                    self.matrix[row[0] + tile_y - 1][item[0] + tile_x] = 8
                if item[1] == 0:
                    self.matrix[row[0] + tile_y][item[0] + tile_x] = np.random.choice(self.tile_ids,
                                                                                      p=self.tile_probabilities)
            continue

        self.pos.move_towards_ip(pygame.Vector2(self.rect.x - v_x, self.rect.y - v_y), player.speed / fps)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        """
        1-4 - трава
        5   - пенек
        6   - куст
        7   - нижняя часть дерева
        8   - верхняя часть дерева
        """

    def draw(self):
        tile_x, tile_y = 0, 0
        while self.rect.x + tile_x * 64 < -64:
            tile_x += 1
        while self.rect.y + tile_y * 64 < -64:
            tile_y += 1
        for row in enumerate(self.matrix[tile_y:tile_y + 18]):
            for item in enumerate(row[1][tile_x:tile_x + 31]):
                if (self.rect.x + (item[0] + tile_x) * 64 > 1920 or self.rect.x + (item[0] + tile_x) * 64 < -64 or
                        self.rect.y + (row[0] + tile_y) * 64 > 1080 or self.rect.y + (row[0] + tile_y) * 64 < -64):
                    continue
                if item[1] == 0:
                    continue
                elif item[1] == 1:
                    image = self.grass_1
                elif item[1] == 2:
                    image = self.grass_2
                elif item[1] == 3:
                    image = self.grass_3
                elif item[1] == 4:
                    image = self.grass_4
                elif item[1] == 5:
                    image = self.stomp
                elif item[1] == 6:
                    image = self.bush
                elif item[1] == 7:
                    image = self.tree_1
                else:
                    image = self.tree_2
                screen.blit(image, (self.rect.x + (item[0] + tile_x) * 64, self.rect.y + (row[0] + tile_y) * 64))

    def draw_tree_over(self):
        tile_x, tile_y = 0, 0
        while self.rect.x + tile_x * 64 < -64:
            tile_x += 1
        while self.rect.y + tile_y * 64 < -64:
            tile_y += 1
        for row in enumerate(self.matrix[tile_y:tile_y + 18]):
            for item in enumerate(row[1][tile_x:tile_x + 31]):
                if item[1] == 7:
                    image = self.tree_1_top
                elif item[1] == 8:
                    image = self.tree_2_top
                else:
                    continue
                screen.blit(image, (self.rect.x + (item[0] + tile_x) * 64, self.rect.y + (row[0] + tile_y) * 64))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hp, weapons):
        super().__init__()
        self.image = load_image('player.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = 140
        self.v_x = 0  # скорость по x
        self.v_y = 0  # скорость по y
        self.hp = hp
        self.max_hp = hp
        self.weapons = weapons
        self.experience = 0
        self.level = 0
        self.walk_sound = pygame.mixer.Sound("data/sounds/player_walking.wav")
        self.walk_sound.set_volume(0.6)
        self.walk_cooldown = 400
        self.upgrades = [["damage", 0, 6, "+15%"], ["projectile speed", 0, 5, "+20%"],
                         ["movement speed", 0, 4, "+15%"], ["fire rate", 0, 6, "+12%"],
                         ["projectile size", 0, 4, "+20%"], ["max hp", 0, 5, "+30%"],["hp regen", 0, 4, "+40%"],
                         ["projectile amount", 0, 3, "+1"], ["experience gain", 0, 5, "+20%"]]
        self.timer = 0
        self.pause_timer = 3000
        self.pos = pygame.Vector2(size[0] // 2 - width // 2, size[1] // 2 - height // 2)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, width, height)
        self.frames = []
        self.cut_sheet(load_image("player.png", -1), 2, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame][0]
        self.image = pygame.transform.scale(self.image, (width, height))
        self.walking = False
        self.direction = False
        self.stats = {"time survived": "",
                      "wave reached": 0,
                      "damage dealt": 0,
                      "damage taken": 0,
                      "enemies slain": 0,
                      "upgrades gotten": 0,}
        self.dir = 1
        #  1 2 3
        #   \|/
        #  4-*-5
        #   /|\
        #  6 7 8

    def cut_sheet(self, sheet, columns, rows):
        rrect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rrect.w * i, rrect.h * j)
                item = sheet.subsurface(pygame.Rect(frame_location, rrect.size))
                item = pygame.transform.scale(item, (self.rect.width, self.rect.height))
                item1 = item.copy()
                item1 = pygame.transform.flip(item1, True, False)
                self.frames.append((item, item1))

    def update(self):
        self.pause_timer -= clock.get_time()
        if self.walking:
            self.timer += clock.get_time()
        if self.timer >= 175:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.timer = 0
        if self.direction:
            self.image = self.frames[self.cur_frame][0]
        else:
            self.image = self.frames[self.cur_frame][1]
        self.max_hp = 100 * (1 + 0.3 * self.upgrades[5][1])
        self.v_x, self.v_y = 0, 0
        self.hp += 0.5 * (1 + 0.4 * self.upgrades[6][1]) / fps
        enemy_collisions = pygame.sprite.spritecollide(self, enemies, False)
        for collision in enemy_collisions:
            if pygame.sprite.collide_mask(self, collision):
                self.hp -= collision.damage / fps
                self.stats["damage taken"] = self.stats["damage taken"] + collision.damage / fps
        if self.experience > 30 * self.level ** 1.08 + 45:
            self.gain_experience(0)
        if self.hp < 0:
            game_over()
            self.kill()
        for weapon in self.weapons:
            weapon.update()


    def key_down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.v_x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.v_x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.v_y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.v_y += self.speed
        if (keys[pygame.K_ESCAPE] or keys[pygame.K_p] or keys[pygame.K_SPACE]) and self.pause_timer < 0:
            print(self.pause_timer)
            pause()
        if keys[pygame.K_k]:
            self.hp -= 500
        if abs(self.v_x) + abs(self.v_y) > self.speed:  # это чтобы персонаж не двигался быстро по диагонали
            self.v_x = 0.6 * self.speed if self.v_x > 0 else -0.6 * self.speed
            self.v_y = 0.6 * self.speed if self.v_y > 0 else -0.6 * self.speed
        tile_x, tile_y = 0, 0
        while mp.rect.x + tile_x * 64 < -64:
            tile_x += 1
        while mp.rect.y + tile_y * 64 < -64:
            tile_y += 1
        for row in enumerate(mp.matrix[tile_y:tile_y + 18]):
            for item in enumerate(row[1][tile_x:tile_x + 31]):
                if item[1] == 5 or item[1] == 7:
                    rect = pygame.Rect(item[0] * 64 + mp.rect.x % 64 - 49, row[0] * 64 + mp.rect.y % 64 - 50, 36, 43)
                    if pygame.Rect.colliderect(self.rect, rect):
                        if self.rect.y + 5 > rect.y:
                            self.v_y += 1
                        else:
                            self.v_y -= 1
                        continue
                    self.pos.move_towards_ip(pygame.Vector2(self.rect.x + self.v_x, self.rect.y + self.v_y),
                                             self.speed / fps)
                    rect_self = pygame.Rect(self.pos.x, self.pos.y, self.rect.width, self.rect.height + 1)
                    if pygame.Rect.colliderect(rect_self, rect):
                        if self.rect.x + 1 > rect.x + rect.width or self.rect.x + self.rect.width < rect.x + 1:
                            self.v_x = 0
                        if self.rect.y + 1 > rect.y + rect.height or self.rect.y + self.rect.height < rect.y + 1:
                            self.v_y = 0
                    self.pos.x = self.rect.x
                    self.pos.y = self.rect.y
        self.walk_cooldown -= clock.get_time()
        if (abs(self.v_x) > 10 or abs(self.v_y) > 10) and self.walk_cooldown <= 0:
            pygame.mixer.find_channel(True).play(self.walk_sound)
            self.walk_cooldown = 400
        self.v_x *= (1 + 0.15 * self.upgrades[5][1])
        self.v_y *= (1 + 0.15 * self.upgrades[5][1])
        if self.v_x == 0 and self.v_y == 0:
            self.walking = False
        else:
            self.walking = True
        if self.v_x > 0:
            self.direction = False
        elif self.v_x < 0:
            self.direction = True
        if self.v_x < 0 and self.v_y < 0:
            self.dir = 1
        elif self.v_x > 0 > self.v_y:
            self.dir = 3
        elif self.v_x < 0 < self.v_y:
            self.dir = 6
        elif self.v_x > 0 and self.v_y > 0:
            self.dir = 8
        elif self.v_y < 0:
            self.dir = 2
        elif self.v_y > 0:
            self.dir = 7
        elif self.v_x < 0:
            self.dir = 4
        elif self.v_x > 0:
            self.dir = 5
        return float(self.v_x), float(self.v_y)

    def gain_experience(self, amt):
        self.experience += amt * (1 + 0.2 * self.upgrades[8][1])
        if self.experience >= 30 * self.level ** 1.08 + 45:
            self.experience -= (30 * self.level ** 1.08 + 45)
            self.level += 1
            level_up()
            while self.experience >= 30 * self.level ** 1.08 + 45:
                self.experience -= (30 * self.level ** 1.08 + 45)
                self.level += 1
                level_up()

    def draw(self):
        screen.blit(player.image, (player.rect.x, player.rect.y))

        pygame.draw.rect(screen, (50, 200, 50), (self.rect.x, self.rect.y + self.rect.height + 5,
                                                 self.rect.width, 15))
        pygame.draw.rect(screen, (200, 50, 50), (self.rect.x + (self.hp / self.max_hp) * self.rect.width + 1,
                                                 self.rect.y + self.rect.height + 5,
                                                 self.rect.width - (self.hp / self.max_hp) * self.rect.width, 15))
        mp.draw_tree_over()

        text = myfont_32.render(f"lvl {self.level}", 1, (255, 50, 50))
        screen.blit(text, (1770, 5))



class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, hp, damage, speed, exp_drop):
        super().__init__()
        self.speed = speed
        self.damage = damage
        self.hp = hp
        self.max_hp = hp
        self.death_sound = pygame.mixer.Sound("data/sounds/enemy_kill.wav")
        self.death_sound.set_volume(0.7)
        self.frames = []
        self.cut_sheet(load_image(image), 4 if image == "enemies/apollo_gasket.png" else 2,
                       3 if image == "enemies/apollo_gasket.png" else 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)
        self.timer = 0
        self.exp_drop = exp_drop

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, v_x, v_y):
        self.timer += clock.get_time()
        if self.timer >= 250:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.timer = 0
        self.image = self.frames[self.cur_frame]
        if self.hp < 0:
            experience = ExperienceShard("experience_shard", self.rect.x + self.rect.width // 2,
                                         self.rect.y + self.rect.height // 2, 19, 25, self.exp_drop)
            items.add(experience)
            pygame.mixer.find_channel(True).play(self.death_sound)
            player.stats["enemies slain"] = player.stats["enemies slain"] + 1
            self.kill()

        self.pos.move_towards_ip(pygame.Vector2(self.rect.x - v_x, self.rect.y - v_y), player.speed / fps)
        self.pos.move_towards_ip(pygame.Vector2(960 - player.rect.width // 2, 540 - player.rect.height // 2),
                                 self.speed / fps)
        collisions = pygame.sprite.spritecollide(Box(self.rect.x + self.rect.width / 4,
                                                     self.rect.y + self.rect.height / 4,
                                                     self.rect.width / 2, self.rect.height / 2),
                                                 enemies, False)
        for collision in collisions:
            if self.rect != collision.rect:
                self.pos.move_towards_ip(pygame.Vector2(collision.pos.x + collision.rect.width / 2,
                                                        collision.pos.y + collision.rect.height / 2),
                                         -(self.speed / 2) / fps)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        surface = pygame.Surface((self.rect.width + 20, 15), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, (0, 0, 0, 50),(0, 0, self.rect.width + 20, 15))
        screen.blit(surface, (self.rect.x - 10, self.rect.y + self.rect.height + 10))


class Knife(pygame.sprite.Sprite):
    def __init__(self, name, x, y, width, height, angle, speed, damage):
        super().__init__()
        self.angle = angle
        self.image = load_image(name)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image = pygame.transform.rotate(self.image, -angle + 180)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = max(width, height)
        self.rect.height = max(width, height)
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)
        self.damage = damage
        self.enemy_hit_sound = pygame.mixer.Sound("data/sounds/enemy_hit.wav")
        self.enemy_hit_sound.set_volume(0.3)

    def update(self, v_x, v_y):
        self.pos.move_towards_ip(pygame.Vector2(self.rect.x - v_x, self.rect.y - v_y), player.speed / fps)
        move_vec = pygame.math.Vector2()
        move_vec.from_polar((self.speed / 60, self.angle))
        self.pos += move_vec
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        enemy_collisions = pygame.sprite.spritecollide(self, enemies, False)
        for collision in enemy_collisions:
            if pygame.sprite.collide_mask(self, collision):
                collision.hp -= self.damage
                player.stats["damage dealt"] = player.stats["damage dealt"] + self.damage
                damage_text = DamageNumber(self.rect.x + self.rect.width // 2,
                                           self.rect.y + self.rect.height // 2,
                                           self.damage)
                texts.add(damage_text)
                pygame.mixer.find_channel(True).play(self.enemy_hit_sound)
                self.kill()


class Weapon:
    def __init__(self, proj_name, proj_width, proj_height, proj_speed, proj_damage, reload_time, time_ibs):
        self.proj_height = proj_height
        self.proj_width = proj_width
        self.proj_damage = proj_damage
        self.proj_speed = proj_speed
        self.proj_name = proj_name
        self.reload_time = reload_time
        self.time_ibs = time_ibs


class Item(pygame.sprite.Sprite):
    def __init__(self, name, x, y, width, height):
        super().__init__()
        self.image = load_image(f'{name}.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = pygame.Vector2(x, y)

    def move(self, x, y, speed):
        self.pos.move_towards_ip(pygame.Vector2(x, y), speed)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class ExperienceShard(Item):
    def __init__(self, name, x, y, width, height, amt):
        super().__init__(name, x, y, width, height)
        self.amt = amt
        self.pickup_sound = pygame.mixer.Sound("data/sounds/pickup.wav")

    def update(self, v_x, v_y):
        self.pos.move_towards_ip(pygame.Vector2(self.rect.x - v_x, self.rect.y - v_y), player.speed / fps)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.pos.distance_to(pygame.Vector2(player.rect.x + player.rect.width // 2,
                                               player.rect.y + player.rect.height // 2)) < 50:
            player.gain_experience(self.amt)
            pygame.mixer.find_channel(True).play(self.pickup_sound)
            self.kill()
        elif self.pos.distance_to(pygame.Vector2(player.rect.x + player.rect.width // 2,
                                               player.rect.y + player.rect.height // 2)) < 200:
            self.move(player.rect.x + player.rect.width // 2, player.rect.y + player.rect.height // 2, 5)
        screen.blit(self.image, (self.pos.x, self.pos.y))


class DamageNumber(pygame.sprite.Sprite):
    def __init__(self, x, y, damage):
        super().__init__()
        self.text = myfont_32.render(f"-{math.floor(damage)}", 1, (220, 0, 0))
        self.rect = pygame.Rect(x, y, 0, 0)
        self.pos = pygame.Vector2(x, y)
        self.text_timer = 500

    def update(self, v_x, v_y, *args):
        self.pos.move_towards_ip(pygame.Vector2(self.rect.x - v_x, self.rect.y - v_y), player.speed / fps * 0.8)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        screen.blit(self.text, (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        self.text_timer -= clock.get_time()
        if self.text_timer < 0:
            self.kill()


class Knives(Weapon):
    def shoot(self):
        try:
            enemies1 = sorted([e for e in enemies], key=lambda e:
            player.pos.distance_to(pygame.math.Vector2(e.rect.x + e.rect.width / 2, e.rect.y + e.rect.height / 2)))
            found_enemy = False
            for enemy1 in enemies1:
                if enemy1.rect.x < 0 or enemy1.rect.x > 1920 or enemy1.rect.y < 0 or enemy1.rect.y > 1080:
                    continue
                else:
                    found_enemy = True
                    enemy = enemy1
                    break
            if not found_enemy:
                return
            dx, dy = (enemy.rect.x + enemy.rect.width / 2) - (player.rect.x + player.rect.width / 2), (
                        enemy.rect.y + enemy.rect.height / 2) - (player.rect.y + player.rect.height / 2)
            angle = math.degrees(math.atan2(dy, dx))
            if angle < 0:
                angle += 360
            projectile = Knife(self.proj_name,
                                    player.rect.x + player.rect.width / 2 + randint(-10, 10),
                                    player.rect.y + player.rect.height / 2 + randint(-10, 10),
                                    self.proj_width * (1 + 0.2 * player.upgrades[4][1]),
                                    self.proj_height * (1 + 0.2 * player.upgrades[4][1]), angle,
                                    self.proj_speed * (1 + 0.2 * player.upgrades[1][1]),
                                    self.proj_damage * (1 + 0.15 * player.upgrades[0][1]))
            projectiles.add(projectile)
        except ValueError:
            pass

    def update(self):
        self.reload_time -= clock.get_time()
        if self.reload_time <= 0:
            self.shoot()
            for i in range(player.upgrades[7][1]):
                while self.time_ibs > 0:
                    self.time_ibs -= clock.get_time()
                self.time_ibs = 300
                self.shoot()
            self.reload_time = 1000 * (1 - 0.12 * player.upgrades[3][1])


class Sword(Weapon):
    def __init__(self, proj_name, proj_width, proj_height, proj_speed, proj_damage, reload_time, time_ibs):
        super().__init__(proj_name, proj_width, proj_height, proj_speed, proj_damage, reload_time, time_ibs)
        self.image = None
        self.pos = pygame.Vector2(size[0] // 2, size[1] // 2 - 50)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 0, 0)
        self.frames = []
        self.cut_sheet(load_image("projectiles/sword_atk.png", -1), 3, 3)
        self.cur_frame = 0
        self.time_ibs = time_ibs


    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        self.frames.append(tuple(frames))
        frames = [pygame.transform.flip(frame, True, False) for frame in frames]
        self.frames.append(tuple(frames))

    def scale(self):
        self.frames = [tuple(pygame.transform.scale(frame, (100 * (1 + 0.2 * player.upgrades[4][1]),
                                                            100 * (1 + 0.2 * player.upgrades[4][1])))
                             for frame in frames) for frames in self.frames]

    def shoot(self):
        projectile = SwordAtk(self.frames[1] if player.direction else self.frames[0],
                           player.rect.x + player.rect.width / 2 - 115 if player.direction
                           else player.rect.x + player.rect.width / 2 + 15,
                           player.rect.y + player.rect.height / 2 - 50,
                           self.proj_damage * (1 + 0.15 * player.upgrades[0][1]))
        projectiles.add(projectile)


    def update(self, *args):
        self.reload_time -= clock.get_time()
        if self.reload_time <= 0:
            self.shoot()
            for i in range(player.upgrades[7][1]):
                while self.time_ibs > 0:
                    self.time_ibs -= clock.get_time()
                self.time_ibs = 300
                self.shoot()
            self.reload_time = 1400 * (1 - 0.12 * player.upgrades[3][1])


class SwordAtk(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, damage):
        super().__init__()
        self.frames = frames
        self.rect = self.frames[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)
        self.damage = damage
        self.enemy_hit_sound = pygame.mixer.Sound("data/sounds/enemy_hit.wav")
        self.enemy_hit_sound.set_volume(0.3)
        self.timer = 0
        self.collision = True
        self.cur_frame = 1
        self.image = self.frames[3]

    def update(self, v_x, v_y):
        self.timer += clock.get_time()
        self.pos.move_towards_ip(pygame.Vector2(self.rect.x - v_x, self.rect.y - v_y), player.speed / fps)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.timer > 380:
            self.kill()
        elif self.timer > 370:
            self.image = self.frames[8]
        elif self.timer > 360:
            self.image = self.frames[7]
        elif self.timer > 320:
            self.image = self.frames[6]
        elif self.timer > 290:
            self.image = self.frames[5]
        elif self.timer > 260:
            self.image = self.frames[4]
        elif self.timer > 210:
            self.image = self.frames[3]
            if self.collision:
                enemy_collisions = pygame.sprite.spritecollide(self, enemies, False)
                for collision in enemy_collisions:
                    if pygame.sprite.collide_mask(self, collision):
                        collision.hp -= self.damage
                        player.stats["damage dealt"] = player.stats["damage dealt"] + self.damage
                        damage_text = DamageNumber(self.rect.x + self.rect.width // 2,
                                                   self.rect.y + self.rect.height // 2,
                                                   self.damage)
                        texts.add(damage_text)
                        pygame.mixer.find_channel(True).play(self.enemy_hit_sound)
                self.collision = False
        elif self.timer > 170:
            self.image = self.frames[3]
        elif self.timer > 140:
            self.image = self.frames[2]
        elif self.timer > 80:
            self.image = self.frames[1]
        elif self.timer > 0:
            self.image = self.frames[0]


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)


pygame.init()
pygame.display.set_caption("Vampire Survivors на минималках")
size = [1920, 1080]  # размер окна

pygame.mixer.init(channels=512)

screen = pygame.display.set_mode(size, pygame.SRCALPHA)
colors = [pygame.Color("white"), pygame.Color("black")]
screen.fill(colors[1])

clock = pygame.time.Clock()
fps = 60

pygame.font.init()
font_path = "data/Monocraft.ttc"
font_size = 64
myfont_64 = pygame.font.Font(font_path, font_size)
myfont_32 = pygame.font.Font(font_path, 32)
myfont_48 = pygame.font.Font(font_path, 48)
myfont_128 = pygame.font.Font(font_path, 128)

MUSIC_END = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(MUSIC_END)
pygame.mixer.music.load("data/OST.wav")

mp = Map("default_map2.png")
knives = Knives("projectiles/knife.png", 50, 30, 350, 7, 1000, 300)
sword = Sword("projectiles/sword_atk.png", 60, 40, 350, 25, 1400, 300)
player = Player(1000, 500, 60, 100, 100, [knives, sword])
spawner = EnemySpawner()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
items = pygame.sprite.Group()
texts = pygame.sprite.Group()

pygame.mixer.music.play()

main_menu()

t = True

def game_loop():
    running = True
    while running:
        screen.fill(colors[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == MUSIC_END:
                pygame.mixer.music.play()
        v_x, v_y = player.key_down()
        mp.update(v_x, v_y)
        mp.draw()

        projectiles.update(v_x, v_y)
        projectiles.draw(screen)

        items.update(v_x, v_y)
        items.draw(screen)

        player.update()
        player.draw()

        enemies.update(v_x, v_y)
        enemies.draw(screen)

        draw_experience_bar()

        texts.update(v_x, v_y)
        spawner.update()

        time = pygame.time.get_ticks() // 1000
        time = (f"{time // 60 if time > 600 else '0' + str(time // 60) if time > 60 else '00'}:"
                f"{time % 60 if time % 60 > 9 else '0' + str(time % 60)}")
        player.stats["time survived"] = time
        text = myfont_64.render(time, 1, (200, 0, 0))
        screen.blit(text, (960 - text.get_width() / 2, 100))

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()

game_loop()