import pygame
import random

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('kek')

cactus_img = [
    pygame.image.load('images/Objects/Cactus0.png'),
    pygame.image.load('images/Objects/Cactus1.png'),
    pygame.image.load('images/Objects/Cactus2.png')
]
cactus_options = [
    69, 449, 37, 410, 40, 420
]

stone_img = [
    pygame.image.load('images/Objects/Stone0.png'),
    pygame.image.load('images/Objects/Stone1.png')
]

cloud_img = [
    pygame.image.load('images/Objects/Cloud0.png'),
    pygame.image.load('images/Objects/Cloud1.png')
]

dino_img = [
    pygame.image.load('images/Dino/Dino0.png'),
    pygame.image.load('images/Dino/Dino1.png'),
    pygame.image.load('images/Dino/Dino2.png'),
    pygame.image.load('images/Dino/Dino3.png'),
    pygame.image.load('images/Dino/Dino4.png')
]

img_counter = 0


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image

        display.blit(self.image, (self.x, self.y))


usr_width = 60
usr_height = 100
usr_x = display_width // 3
usr_y = display_height - usr_height - 100

cactus_width = 20
cactus_height = 70
cactus_x = display_width - 50
cactus_y = display_height - cactus_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30


def run_game():
    global make_jump

    game = True

    cactus_arr = []

    create_cactus_arr(cactus_arr)

    land = pygame.image.load('images/Backgrounds/Land.jpg')

    stone, cloud = open_random_objects()

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            make_jump = True

        if make_jump:
            jump()

        display.blit(land, (0, 0))
        draw_array(cactus_arr)
        move_objects(stone, cloud)

        # pygame.draw.rect(display, (247, 240, 22), (usr_x, usr_y, usr_width, usr_height))
        draw_dino()

        pygame.display.update()

        clock.tick(80)


def jump():
    global usr_y, make_jump, jump_counter

    if jump_counter >= -30:
        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)

    img = cactus_img[choice]

    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]

    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)

    img = cactus_img[choice]

    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]

    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)

    img = cactus_img[choice]

    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]

    array.append(Object(display_width + 600, height, width, img, 4))


def find_radius(array):
    maximum = max(array[0].x,
                  array[1].x,
                  array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum

    choise = random.randrange(0, 5)

    if not choise:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 250)

    return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]

            cactus.return_self(radius, height, width, img)


def open_random_objects():
    choice = random.randrange(0, 1)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 1)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
    cloud = Object(display_width, 80, 70, img_of_cloud, 2)

    return stone, cloud


def move_objects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10, 200), stone.width, img_of_cloud)


def draw_dino():
    global img_counter

    if img_counter == 25:
        img_counter = 0

    display.blit(dino_img[img_counter // 5], (usr_x, usr_y))
    img_counter += 1


run_game()
