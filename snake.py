import pygame
import random
import tkinter as tk
from tkinter import messagebox


class Cube:
    def __init__(self, start, cube_size, rows, color=(255, 0, 0)):
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
            circlemiddle = (column*cs+center-radius, row*cs+8)
            circlemiddle2 = (column*cs+cs-radius*2, row*cs+8)
            pygame.draw.circle(win, (0, 0, 0), circlemiddle, radius)
            pygame.draw.circle(win, (0, 0, 0), circlemiddle2, radius)


class Snake:
    def __init__(self, color, position, size, rows):
        self.body = []
        self.turns = {}
        self.color = color
        self.rows = rows
        self.snake_size = size
        self.head = Cube(position, self.snake_size, self.rows)
        self.body.append(self.head)

    def move(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            dirnx = -1
            dirny = 0
            self.turns[self.head.position] = (dirnx, dirny)
        elif keys[pygame.K_RIGHT]:
            dirnx = 1
            dirny = 0
            self.turns[self.head.position] = (dirnx, dirny)
        elif keys[pygame.K_UP]:
            dirnx = 0
            dirny = - 1
            self.turns[self.head.position] = (dirnx, dirny)
        elif keys[pygame.K_DOWN]:
            dirnx = 0
            dirny = 1
            self.turns[self.head.position] = (dirnx, dirny)

        for i, c in enumerate(self.body):
            p = c.position
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


def randomcube(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.position == (x, y), positions))) > 0:
            continue
        else:
            return x, y


def refresh_board(win, width, snake, step_size, snack):
    win.fill((0, 0, 0))
    snake.draw_snake(win)
    snack.draw(win)
    draw_grid(win, step_size, width)
    pygame.display.update()


def message_box(sub, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(sub, content)


def game_loop():
    height, width = 500, 500
    rows = 20
    step_size = width // rows

    pygame.init()
    win = pygame.display.set_mode(size=(height, width))
    snake = Snake((255, 0, 0), (10, 10), step_size, rows)  # Create the snakehead on its starting position
    snack = Cube(randomcube(rows, snake), step_size, rows, color=(0, 255, 0))
    x = True

    clock = pygame.time.Clock()
    while x:

        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.body[0].position == snack.position:
            snake.addcube()
            snack = Cube(randomcube(rows, snake), step_size, rows, color=(0, 255, 0))

        for i in range(len(snake.body)):
            if snake.body[i].position in list(map(lambda s: s.position, snake.body[i+1:])):
                print("Score: ", len(snake.body))
                message_box("You lost", "Play again")
                snake = Snake((255, 0, 0), (10, 10), step_size, rows)
                break

        refresh_board(win, height, snake, step_size, snack)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


if __name__ == "__main__":
    game_loop()

    # elif event.type == pygame.KEYDOWN:
    # if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
    #    print(event.key)
    # key = pygame.key.get_pressed()
    # if key[pygame.K_a]:
    #   x = False
