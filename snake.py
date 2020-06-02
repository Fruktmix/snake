import pygame, random


class Cube:
    # rows = 20 # TODO denna behövs nog inte heller
    def __init__(self, start, cube_size, rows, dirnx=1, dirny=0, color=(255, 0, 0)): # TODO dirnx/y här behövs nog inte
        self.position = start
        self.dirnx = 1  # Initial X movement
        self.dirny = 0  # Initial Y movement
        self.cube_size = cube_size
        self.color = color
        self.rows = rows

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.position = (self.position[0] + self.dirnx, self.position[1] + self.dirny)

    def draw(self, win, eyes=False):
        cs = self.cube_size
        column = self.position[0]
        row = self.position[1]

        pygame.draw.rect(win, self.color, (column*cs+1, row*cs+1, cs-2, cs-2))
        if eyes:
            center = cs // 2
            radius = 3
            circleMiddle = (column*cs+center-radius, row*cs+8)
            circleMiddle2 = (column*cs+cs-radius*2, row*cs+8)
            pygame.draw.circle(win, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(win, (0, 0, 0), circleMiddle2, radius)


class Snake:
    body = [] # TODO dessa borde vara intsansvariabler
    turns = {}

    def __init__(self, color, position, size, rows):
        self.color = color
        self.rows = rows
        self.snake_size = size
        self.head = Cube(position, self.snake_size, self.rows)
        self.body.append(self.head)


        self.dirnx = 0  # Initial X movement
        self.dirny = 1  # Initial Y movement # TODO Dessa behövs nog inte

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                exit()

            keys = pygame.key.get_pressed()

            #for key in keys: # TODO denna ser inte heller ut att behövas
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny] # TODO Tror inte att man måste göra kopior på kordinaterna här då de bara är en nyckel
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = - 1
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny] # TODO dettta borde kunna generaliseras
            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.position[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.position[0] <= 0:
                    c.position = (c.rows - 1, c.position[1])
                elif c.dirnx == 1 and c.position[0] >= c.rows - 1:
                    c.position = (0, c.position[1])
                elif c.dirny == 1 and c.position[1] >= c.rows - 1:
                    c.position = (c.position[0], 0)
                elif c.dirny == -1 and c.position[1] <= 0:
                    c.position = (c.position[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def addcube(self):
        tail = self.body[-1]
        dirnx, dirny = tail.dirnx, tail.dirny

        if dirnx == 1 and dirny == 0:
            self.body.append(Cube((tail.position[0]-1, tail.position[1]), self.snake_size, self.rows))
        elif dirnx == -1 and dirny == 0:
            self.body.append(Cube((tail.position[0]+1, tail.position[1]), self.snake_size, self.rows))
        elif dirnx == 0 and dirny == 1:
            self.body.append(Cube((tail.position[0], tail.position[1]-1), self.snake_size, self.rows))
        elif dirnx == 0 and dirny == -1:
            self.body.append(Cube((tail.position[0], tail.position[1]+1), self.snake_size, self.rows))

        self.body[-1].dirnx, self.body[-1].dirny = dirnx, dirny


    def draw_snake(self, win):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(win, True)
            else:
                c.draw(win)


def draw_grid(win, step_size, width):

    x, y = 0, 0
    for row in range(width//step_size):
        x += step_size
        y += step_size

        pygame.draw.line(win, (255, 255, 255), (x, 0), (x, width))  # Vertical line
        pygame.draw.line(win, (255, 255, 255), (0, y), (width, y))  # Horizontal line


def randomCube(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.position == (x, y), positions))) > 0: # TODO Denna ska ändras, kollar så att ett snack inte spawnar på ormen.
            continue
        else:
            break  # TODO förbättra denna
    return x, y


def refresh_board(win, width, snake, step_size, snack):
    win.fill((0, 0, 0))
    snake.draw_snake(win)
    snack.draw(win)
    draw_grid(win, step_size, width)
    pygame.display.update()


def game_loop():
    height, width = 500, 500
    rows = 20
    step_size = width // rows

    pygame.init()
    win = pygame.display.set_mode(size=(height, width))
    snake = Snake((255, 0, 0), (10, 10), step_size, rows)  # Create the snakehead on its starting position
    snack = Cube(randomCube(rows, snake), step_size, rows, color=(0, 255, 0))
    x = True

    clock = pygame.time.Clock()
    while x:

        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.body[0].position == snack.position:
            snake.addcube()
            snack = Cube(randomCube(rows, snake), step_size, rows, color=(0, 255, 0))
        refresh_board(win, height, snake, step_size, snack)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                exit()


if __name__ == "__main__":
    game_loop()

    #elif event.type == pygame.KEYDOWN:
    #if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
    #    print(event.key)
    #key = pygame.key.get_pressed()
    #if key[pygame.K_a]:
    #   x = False