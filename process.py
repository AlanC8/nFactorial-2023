import random
import pygame

pygame.init()
start_ticks = pygame.time.get_ticks()

level = random.randint(1, 4)

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)

size = (701, 701)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Maze Generator")
# bg = pygame.image.load("bg.png")
# bg = pygame.transform.scale(bg, (701,701))
done = False

clock = pygame.time.Clock()

width = 25 * level
if level == 3:
    width = 23 * level
cols = int(size[0] / width)
rows = int(size[1] / width)
print(level)
stack = []

pos = (0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos, background):
        super().__init__()
        self.image = image
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.background = background

    def update(self, events, dt):
        pressed = pygame.key.get_pressed()
        move = pygame.Vector2((0, 0))

        # calculate maximum movement and current cell position
        testdist = dt // 5 + 2
        cellx = self.rect.centerx // width
        celly = self.rect.centery // width
        minx = self.rect.left // width
        maxx = self.rect.right // width
        miny = self.rect.top // width
        maxy = self.rect.bottom // width

        # test move up
        if minx == maxx and pressed[pygame.K_w]:
            nexty = (self.rect.top - testdist) // width
            if celly == nexty or (nexty >= 0 and not grid[celly][cellx].walls[0]):
                move += (0, -1)

        # test move right
        elif miny == maxy and pressed[pygame.K_d]:
            nextx = (self.rect.right + testdist) // width
            if cellx == nextx or (nextx < cols and not grid[celly][cellx].walls[1]):
                move += (1, 0)

        # test move down
        elif minx == maxx and pressed[pygame.K_s]:
            nexty = (self.rect.bottom + testdist) // width
            if celly == nexty or (nexty < rows and not grid[celly][cellx].walls[2]):
                move += (0, 1)

                # test move left
        elif miny == maxy and pressed[pygame.K_a]:
            nextx = (self.rect.left - testdist) // width
            if cellx == nextx or (nextx >= 0 and not grid[celly][cellx].walls[3]):
                move += (-1, 0)

        self.pos = self.pos + move * (dt / 5)
        self.rect.center = self.pos


def load_background(filename=None):
    name = filename if filename else "background.jpg"
    background = pygame.image.load("background.png")
    background = pygame.transform.scale(background, (701, 701))
    return background


def load_player(background):
    pimg = pygame.Surface((10, 10))
    pimg.fill(pygame.Color("blue"))

    px = 680
    py = 680
    return Player(pimg, (px, py), background)


class Cell():
    def __init__(self, x, y):
        global width
        self.x = x * width
        self.y = y * width

        self.visited = False
        self.current = False

        self.walls = [True, True, True, True]  # top , right , bottom , left

        # neighbors
        self.neighbors = []

        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0

        self.next_cell = 0

    def draw(self):
        if self.current:
            pygame.draw.rect(screen, RED, (self.x, self.y, width, width))
        elif self.visited:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, width, width))

            if self.walls[0]:
                pygame.draw.line(screen, BLACK, (self.x, self.y),
                                 ((self.x + width), self.y), 1)  # top
            if self.walls[1]:
                pygame.draw.line(screen, BLACK, ((self.x + width), self.y),
                                 ((self.x + width), (self.y + width)), 1)  # right
            if self.walls[2]:
                pygame.draw.line(screen, BLACK, ((
                                                         self.x + width), (self.y + width)), (self.x, (self.y + width)),
                                 1)  # bottom
            if self.walls[3]:
                pygame.draw.line(
                    screen, BLACK, (self.x, (self.y + width)), (self.x, self.y), 1)  # left

    def checkNeighbors(self):
        # print("Top; y: " + str(int(self.y / width)) + ", y - 1: " + str(int(self.y / width) - 1))
        if int(self.y / width) - 1 >= 0:
            self.top = grid[int(self.y / width) - 1][int(self.x / width)]
        # print("Right; x: " + str(int(self.x / width)) + ", x + 1: " + str(int(self.x / width) + 1))
        if int(self.x / width) + 1 <= cols - 1:
            self.right = grid[int(self.y / width)][int(self.x / width) + 1]
        # print("Bottom; y: " + str(int(self.y / width)) + ", y + 1: " + str(int(self.y / width) + 1))
        if int(self.y / width) + 1 <= rows - 1:
            self.bottom = grid[int(self.y / width) + 1][int(self.x / width)]
        # print("Left; x: " + str(int(self.x / width)) + ", x - 1: " + str(int(self.x / width) - 1))
        if int(self.x / width) - 1 >= 0:
            self.left = grid[int(self.y / width)][int(self.x / width) - 1]
        # print("--------------------")

        if self.top != 0:
            if self.top.visited == False:
                self.neighbors.append(self.top)
        if self.right != 0:
            if self.right.visited == False:
                self.neighbors.append(self.right)
        if self.bottom != 0:
            if self.bottom.visited == False:
                self.neighbors.append(self.bottom)
        if self.left != 0:
            if self.left.visited == False:
                self.neighbors.append(self.left)

        if len(self.neighbors) > 0:
            self.next_cell = self.neighbors[random.randrange(
                0, len(self.neighbors))]
            return self.next_cell
        else:
            return False


def removeWalls(current_cell, next_cell):
    x = int(current_cell.x / width) - int(next_cell.x / width)
    y = int(current_cell.y / width) - int(next_cell.y / width)
    if x == -1:  # right of current
        current_cell.walls[1] = False
        next_cell.walls[3] = False
    elif x == 1:  # left of current
        current_cell.walls[3] = False
        next_cell.walls[1] = False
    elif y == -1:  # bottom of current
        current_cell.walls[2] = False
        next_cell.walls[0] = False
    elif y == 1:  # top of current
        current_cell.walls[0] = False
        next_cell.walls[2] = False


grid = []

for y in range(rows):
    grid.append([])
    for x in range(cols):
        grid[y].append(Cell(x, y))

current_cell = grid[0][0]
next_cell = 0

# -------- Main Program Loop -----------
pygame.font.init()


def loose():
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        bg = pygame.image.load("background.png")
        bg = pygame.transform.scale(bg, (701, 701))
        screen.blit(bg, (0, 0))
        pygame.display.update()


def youWin():
    winpage = pygame.image.load("win-bg.jpg")
    screen.blit(winpage, (0, 0))
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()


def main():
    global current_cell, grid
    player = None
    initialized = False
    current_maze = None
    dt = 0
    # screen_rect = screen.get_rect()
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    if not initialized:
        # current_maze = 0
        background = load_background()
        background = None
        player = load_player(background)
        sprites.add(player)
        initialized = True

    play = False
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if play == True:

            pygame.draw.rect(screen, PURPLE, player.rect)
            sprites.update(None, dt)
            sprites.draw(screen)

            dt = clock.tick(60)

            finished = pygame.Rect(0, 0, width, width).colliderect(player.rect)
            if finished:
                # init new grid
                grid = []
                for y in range(rows):
                    grid.append([])
                    for x in range(cols):
                        grid[y].append(Cell(x, y))
                current_cell = grid[0][0]
                # create new random player positon
                px = random.randint(0, rows - 1) * width + width // 2
                py = random.randint(0, cols - 1) * width + width // 2
                player.pos = pygame.Vector2(px, py)
                player.rect = player.image.get_rect(center=player.pos)
                # clear screen
                screen.fill(pygame.Color("darkslategray"))
                play = False
                youWin()
        else:
            current_cell.visited = True
            current_cell.current = True

            next_cell = current_cell.checkNeighbors()
            if next_cell != False:
                current_cell.neighbors = []
                stack.append(current_cell)
                removeWalls(current_cell, next_cell)
                current_cell.current = False
                current_cell = next_cell
            elif len(stack) > 0:
                current_cell.current = False
                current_cell = stack.pop()
            else:
                play = True

            for y in range(rows):
                for x in range(cols):
                    grid[y][x].draw()

        if level == 4:
            my_font = pygame.font.SysFont('Comic Sans MS', 24)
            text_surface = my_font.render("You have 30s", False, (0, 0, 0))
            screen.blit(text_surface, (500, 30))
            seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            if (90 - seconds <= 60):
                loose()
        if level == 2 or level == 3:
            my_font = pygame.font.SysFont('Comic Sans MS', 24)
            text_surface = my_font.render("You have 120s", False, (0, 0, 0))
            screen.blit(text_surface, (500, 30))
            seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            if (180 - seconds <= 60):
                loose()
        if level == 1:
            my_font = pygame.font.SysFont('Comic Sans MS', 24)
            text_surface = my_font.render("You have 180s", False, (0, 0, 0))
            screen.blit(text_surface, (500, 30))
            seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            if (240 - seconds <= 60):
                loose()

        pygame.display.flip()


if __name__ == "__main__":
    main()
