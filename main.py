import pygame
import os
import sys
import math
import pytweening

from random import randint


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
    else:
        image = image.convert_alpha()
    return image


class EnemySpawner:
    def __init__(self):
        self.time = 0
        self.interval = 3000

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
        enemy = Enemy(x, y, 90, 120, 10, 10)
        enemies.add(enemy)

    def update(self):
        self.time += clock.get_time()
        if self.time >= self.interval:
            self.spawn_enemy()
            self.time = 0


class Map(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = load_image(name)
        self.speed = 50
        self.v_x = 0  # скорость по x
        self.v_y = 0  # скорость по y
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width / 2 + size[0] / 2
        self.rect.y = -self.rect.height / 2 + size[1] / 2
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)

    def update(self, v_x, v_y):
        self.pos.x -= v_x / fps
        self.pos.y -= v_y / fps
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        screen.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hp, weapons):
        super().__init__()
        self.image = load_image('default_player.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = 70
        self.v_x = 0  # скорость по x
        self.v_y = 0  # скорость по y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)
        self.hp = hp
        self.max_hp = hp
        self.weapons = weapons
        self.experience = 0
        self.level = 0

    def update(self):
        self.pos.move_towards_ip(pygame.Vector2(self.rect.x + self.v_x, self.rect.y + self.v_y), self.speed / 60)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.v_x, self.v_y = 0, 0
        self.hp += 0.5 / 60
        enemy_collisions = pygame.sprite.spritecollide(self, enemies, False)
        for collision in enemy_collisions:
            self.hp -= collision.damage / 60
        screen.blit(player.image, (player.rect.x, player.rect.y))

        pygame.draw.rect(screen, (50, 200, 50), (self.rect.x, self.rect.y  + self.rect.height + 5,
                self.rect.width, 15))
        pygame.draw.rect(screen, (200, 50, 50), (self.rect.x + (self.hp / self.max_hp) * self.rect.width + 1,
                self.rect.y + self.rect.height + 5, self.rect.width - (self.hp / self.max_hp) * self.rect.width, 15))

        pygame.draw.rect(screen, (150, 150, 150), (0, 0, 1920, 40))
        pygame.draw.rect(screen, (14, 110, 251), (0, 0, 1920 *
                                                  (self.experience / (30 * self.level ** 1.08 + 45)), 40))

        text = myfont_32.render(f"lvl {self.level}", 1, (255, 50, 50))
        screen.blit(text, (1770, 5))

    def key_down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.v_x -= self.speed
        if keys[pygame.K_d]:
            self.v_x += self.speed
        if keys[pygame.K_w]:
            self.v_y -= self.speed
        if keys[pygame.K_s]:
            self.v_y += self.speed
        if abs(self.v_x) + abs(self.v_y) > self.speed:  # это чтобы персонаж не двигался быстро по диагонали
            self.v_x = 0.6 * self.speed if self.v_x > 0 else -0.6 * self.speed
            self.v_y = 0.6 * self.speed if self.v_y > 0 else -0.6 * self.speed
        return float(self.v_x), float(self.v_y)

    def shoot(self):
        for weapon in self.weapons:
            weapon.shoot()

    def move_to_center(self):
        self.pos = pygame.Vector2(960 - self.rect.width // 2, 540 - self.rect.height // 2)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def gain_experience(self, amt):
        self.experience += amt
        if self.experience >= 30 * self.level ** 1.08 + 45:
            self.experience = 0
            self.level += 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hp, damage):
        super().__init__()
        self.image = load_image('default_enemy.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = 30
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)
        self.damage = damage
        self.hp = hp
        self.max_hp = hp


    def update(self, v_x, v_y):
        self.pos.x -= v_x / fps
        self.pos.y -= v_y / fps
        self.pos.move_towards_ip(pygame.Vector2(960, 540), self.speed / fps)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.hp < 0:
            experience = ExperienceShard("experience_shard", self.rect.x + self.rect.width // 2,
                                         self.rect.y + self.rect.height // 2, 19, 25, 10)
            items.add(experience)
            self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle, speed, damage):
        super().__init__()
        self.angle = angle
        self.image = load_image('default_projectile.png')
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

    def update(self, v_x, v_y):
        move_vec = pygame.math.Vector2()
        move_vec.from_polar((self.speed / 60, self.angle))
        self.pos += move_vec
        self.pos.x -= v_x / fps
        self.pos.y -= v_y / fps
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        enemy_collisions = pygame.sprite.spritecollide(self, enemies, False)
        for collision in enemy_collisions:
            if pygame.sprite.collide_mask(self, collision):
                collision.hp -= self.damage
                self.kill()

class Weapon:
    def __init__(self, name, proj_width, proj_height, proj_speed, proj_damage):
        self.proj_height = proj_height
        self.proj_width = proj_width
        self.proj_damage = proj_damage
        self.proj_speed = proj_speed
        self.name = name

    def shoot(self):
        try:
            enemy = min([e for e in enemies], key=lambda e: player.pos.distance_to(pygame.math.Vector2(e.rect.x + e.rect.width / 2, e.rect.y + e.rect.height / 2)))
            dx, dy = (enemy.rect.x + enemy.rect.width / 2) - (player.rect.x + player.rect.width / 2), (enemy.rect.y + enemy.rect.height / 2) - (player.rect.y + player.rect.height / 2)
            print(dx, dy)
            if enemy.rect.x < 0 or enemy.rect.x > 1920 or enemy.rect.y < 0 or enemy.rect.y > 1080:
                return
            angle = math.degrees(math.atan2(dy, dx))
            if angle < 0:
                angle += 360
            projectile = Projectile(player.rect.x + player.rect.width / 2, player.rect.y + player.rect.height / 2, self.proj_width, self.proj_height, angle, self.proj_speed, self.proj_damage)
            projectiles.add(projectile)
        except ValueError:
            pass


class Item(pygame.sprite.Sprite):
    def __init__(self, name, x, y, width, height):
        super().__init__()
        self.image = load_image(f'{name}.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y
        self.pos = pygame.Vector2(x, y)

    def move(self, x, y, speed):
        self.pos.move_towards_ip(pygame.Vector2(x, y), speed)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class ExperienceShard(Item):
    def __init__(self, name, x, y, width, height, amt):
        super().__init__(name, x, y, width, height)
        self.amt = amt

    def update(self, v_x, v_y):
        self.pos.x -= v_x / fps
        self.pos.y -= v_y / fps
        if self.pos.distance_to(pygame.Vector2(player.rect.x + player.rect.width // 2,
                                               player.rect.y + player.rect.height // 2)) < 50:
            player.gain_experience(self.amt)
            self.kill()
        elif self.pos.distance_to(pygame.Vector2(player.rect.x + player.rect.width // 2,
                                               player.rect.y + player.rect.height // 2)) < 200:
            self.move(player.rect.x + player.rect.width // 2, player.rect.y + player.rect.height // 2, 10)
        screen.blit(self.image, (self.pos.x, self.pos.y))

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Vampire Survivors на минималках")
    size = [1920, 1080]   #  размер окна

    screen = pygame.display.set_mode(size)
    colors = [pygame.Color("white"), pygame.Color("black")]
    screen.fill(colors[1])

    SPAWNENEMY = pygame.USEREVENT + 1
    SHOOT = pygame.USEREVENT + 2

    running = True
    clock = pygame.time.Clock()
    fps = 60
    map = Map("default_map2.png")
    weapon = Weapon("default_weapon", 60, 20, 350, 1.5)
    player = Player(1000, 500, 85, 100, 100, [weapon])
    spawner = EnemySpawner()
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    items = pygame.sprite.Group()

    pygame.font.init()
    font_path = "data/Monocraft.ttc"
    font_size = 64
    myfont_64 = pygame.font.Font(font_path, font_size)
    myfont_32 = pygame.font.Font(font_path, 32)

    pygame.time.set_timer(SHOOT, 500)
    while running:
        screen.fill(colors[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SHOOT:
                player.shoot()
        v_x, v_y = player.key_down()
        map.update(v_x, v_y)
        spawner.update()
        enemies.update(v_x, v_y)
        enemies.draw(screen)
        player.move_to_center()

        projectiles.update(v_x, v_y)
        projectiles.draw(screen)

        items.update(v_x, v_y)
        items.draw(screen)

        player.update()
        if player.hp < 0:
            print("game over!")
            running = False
        time = pygame.time.get_ticks() // 1000
        time = (f"{time // 60 if time > 600 else "0" + str(time // 60) if time > 60 else "00"}:"
                f"{time % 60 if time % 60 > 9 else "0" + str(time % 60)}")
        text = myfont_64.render(time, 1, (255, 50, 50))
        screen.blit(text, (960 - text.get_width() / 2, 100))

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()