import pygame, random


class Cube:
    def __init__(self, start, cube_size, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.position = start
        self.dirnx = 1  # Initial X movement
        self.dirny = 0  # Initial Y movement
        self.cube_size = cube_size
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.position(self.position[0] + self.dirnx, self.position[1] + self.dirny)

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
    body = []
    turns = {}

    def __init__(self, color, position, size):
        self.color = color
        self.head = Cube(position, size)
        self.body.append(self.head)
        self.snake_size = size

        self.dirnx = 0  # Initial X movement
        self.dirny = 1  # Initial Y movement

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                exit()

            keys = pygame.key.get_pressed()

            #for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = - 1
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def draw_snake(self, win):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(win, True)
            else:
                c.draw(win)


def draw_grid(win, step_size, width):
    # step_size = width // rows

    x, y = 0, 0
    for row in range(width//step_size):
        x += step_size
        y += step_size

        pygame.draw.line(win, (255, 255, 255), (x, 0), (x, width))  # Vertical line
        pygame.draw.line(win, (255, 255, 255), (0, y), (width, y))  # Horizontal line


def refresh_board(win, width, snake, step_size):
    win.fill((0, 0, 0))
    snake.draw_snake(win)
    draw_grid(win, step_size, width)
    pygame.display.update()


def game_loop():
    height, width = 500, 500
    rows = 20
    step_size = width // rows

    pygame.init()
    win = pygame.display.set_mode(size=(height, width))
    snake = Snake((255, 0, 0), (10, 10), step_size)  # Create the snakehead on its starting position
    x = True
    while x:
        refresh_board(win, height, snake, step_size)
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                    print(event.key)
        if key[pygame.K_a]:
            x = False


if __name__ == "__main__":
    game_loop()
