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


def spawn_enemy():
    angle = randint(0, 360)
    enemy = Enemy(math.cos(angle) * randint(400, 700) + player.rect.x,
                  math.sin(angle) * randint(400, 700) + player.rect.y, 90, 120, 10, 10)
    enemies.add(enemy)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hp, weapons):
        super().__init__()
        self.image = load_image('default_player.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = 50
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

    def shoot(self):
        for weapon in self.weapons:
            weapon.shoot()


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


    def update(self):
        self.pos.move_towards_ip(pygame.Vector2(player.rect.x + player.rect.width // 2 - self.rect.width // 2,
                                                player.rect.y + player.rect.height // 2 - self.rect.height // 2),
                                 self.speed / 60)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.hp < 0:
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

    def update(self):
        move_vec = pygame.math.Vector2()
        move_vec.from_polar((self.speed / 60, self.angle))
        self.pos += move_vec
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
            angle = math.degrees(math.atan2(dy, dx))
            if angle < 0:
                angle += 360
            projectile = Projectile(player.rect.x + player.rect.width / 2, player.rect.y + player.rect.height / 2, self.proj_width, self.proj_height, angle, self.proj_speed, self.proj_damage)
            projectiles.add(projectile)
        except ValueError:
            pass

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
    weapon = Weapon("default_weapon", 60, 20, 200, 1.5)
    player = Player(1000, 500, 85, 100, 100, [weapon])
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    pygame.time.set_timer(SPAWNENEMY, 3000)
    pygame.time.set_timer(SHOOT, 500)
    while running:
        screen.fill(colors[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWNENEMY:
                spawn_enemy()
            elif event.type == SHOOT:
                player.shoot()
        player.key_down()
        player.update()
        enemies.update()
        enemies.draw(screen)
        projectiles.update()
        projectiles.draw(screen)
        if player.hp < 0:
            print("game over!")
            running = False
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()