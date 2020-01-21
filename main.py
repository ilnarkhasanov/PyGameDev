import pygame
import random

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dinosaur runs through the desert and scores points')

cactus_img = [
    pygame.image.load('images/updatedObj/cactus1.png'),
    pygame.image.load('images/updatedObj/cactus2.png'),
    pygame.image.load('images/updatedObj/cactus3.png')
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
    pygame.image.load('images/updatedDino/dino1.png').convert_alpha(),
    pygame.image.load('images/updatedDino/dino2.png').convert_alpha(),
    pygame.image.load('images/updatedDino/dino3.png').convert_alpha()
]

img_counter = 0

button_sound = pygame.mixer.Sound('images/Sounds/button.wav')

pygame.mixer.music.set_volume(0.5)


class Button:
    def __init__(self, width, height, inactive_color="", active_color=""):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(display, (200, 200, 200), (x, y, self.width, self.height))

                if click[0] == 1 and action:
                    pygame.mixer.Sound.play(button_sound)
                    pygame.time.delay(300)

                    if action is not None:
                        action()
        else:
            pygame.draw.rect(display, (200, 200, 200), (x, y, self.width, self.height))

        print_text(message, x + 10, y + 10)


def quitGame():
    pygame.quit()
    quit()


def setVolumeOff():
    pygame.mixer.music.set_volume(0)


def setVolumeOn():
    pygame.mixer.music.set_volume(0.5)


def settingsScreen():
    setting_background = pygame.image.load('images/Backgrounds/settings.png')

    show_menu = True

    button = Button(200, 70)

    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(setting_background, (0, 0))

        button.draw(100, 300, 'off', setVolumeOff)
        button.draw(300, 300, 'sound')
        button.draw(500, 300, 'on', setVolumeOn)

        button.draw(10, 10, 'back', startScreen)

        pygame.display.update()
        clock.tick(60)


def startScreen():
    menu_background = pygame.image.load('images/Backgrounds/menu.png')

    start_button = Button(300, 70)

    show_menu = True

    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_background, (0, 0))
        start_button.draw(250, 250, 'Start game', start_game)
        start_button.draw(250, 350, 'Settings', settingsScreen)
        start_button.draw(250, 450, 'Quit game', quitGame)

        pygame.display.update()
        clock.tick(60)


def start_game():
    global scores, make_jump, jump_counter, usr_y

    while game_cycle():
        scores = 0
        make_jump = False
        jump_counter = 30
        usr_y = display_height - usr_height - 90
        pass


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
usr_y = display_height - usr_height - 90

cactus_width = 20
cactus_height = 70
cactus_x = display_width - 50
cactus_y = display_height - cactus_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0
max_scores = 0
max_above = 0

pygame.mixer.music.load('images/Sounds/Double_the_Bits.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(1)


def game_cycle():
    global make_jump

    # startScreen()

    game = True

    cactus_arr = []

    create_cactus_arr(cactus_arr)

    land = pygame.image.load('images/Backgrounds/updatedLand.jpg')

    stone, cloud = open_random_objects()

    button = Button(100, 50, (0, 0, 0), (0, 0, 0))

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        count_scores(cactus_arr)

        display.blit(land, (0, 0))

        print_text("Scores: " + str(scores), 600, 10)

        draw_array(cactus_arr)
        move_objects(stone, cloud)

        draw_dino()

        if check_collision(cactus_arr):
            game = False

        pygame.display.update()

        clock.tick(100)
    return game_over()


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

    if img_counter == 9:
        img_counter = 0

    display.blit(dino_img[img_counter // 3], (usr_x, usr_y))
    img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='images/Effects/MontserratAlternates-SemiBold.ttf',
               font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Press Enter to continue', 220, 300)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)


def check_collision(barriers):
    for barrier in barriers:
        if usr_y + usr_height >= barrier.y:
            if barrier.x <= usr_x <= barrier.x + barrier.width:
                return True
            elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                return True
    return False


def count_scores(barriers):
    global scores, max_above

    above_cactus = 0

    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_height - 5 <= barrier.y:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_cactus += 1
                elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                    above_cactus += 1

        max_above = max(max_above, above_cactus)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0

    if not above_cactus:
        for barrier in barriers:
            if barrier.x <= usr_x + usr_width / 2 <= barrier.x + barrier.width:
                if usr_y + usr_height - 5 <= barrier.y:
                    # above_cactus = True
                    break
    else:
        if jump_counter == -30:
            scores += 1
            # above_cactus = False


def game_over():
    global scores, max_scores

    if scores > max_scores:
        max_scores_file = open('system_files/max_score.txt', 'w')
        max_scores_file.truncate()
        print(scores, file=max_scores_file)
        max_scores_file.close()

        max_scores = scores

        scores = 0

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over. Enter - play again, Escape - quit.', 50, 300)

        get_max_scores = open('system_files/max_score.txt', 'r')
        max_scores = int(get_max_scores.readline())
        get_max_scores.close()

        print_text('Max scores: ' + str(max_scores), 300, 350)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


startScreen()

pygame.quit()
quit()
