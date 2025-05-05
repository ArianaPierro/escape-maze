import random
import pygame


pygame.init()
pygame.font.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650 # Increased height for timer display
CELL_SIZE = 24
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAZE_HEIGHT = (SCREEN_HEIGHT - 50) // CELL_SIZE # Adjusted height for timer display
ENDPOINT = 2
NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (118, 90, 143)
WALL = (65, 77, 58)
PATH = 0
EMPTY = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
EMPTY.fill((255, 0, 255, 0))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
img = pygame.image.load("game_images/exit_door.png").convert_alpha()
exit_door = pygame.transform.scale(img, 
                                  (img.get_width() // 15, 
                                   img.get_height() // 20))
clicked = False
maze = {}
for x in range(MAZE_WIDTH):
    for y in range(MAZE_HEIGHT):
        maze[(x, y)] = 1 # Every space is a wall at first.


def draw_maze(maze):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[(x, y)] == 1:
                pygame.draw.rect(screen, WALL, (x * CELL_SIZE, y * CELL_SIZE,
                                         CELL_SIZE, CELL_SIZE))
            if maze[(x, y)] == PATH:
                screen.blit(EMPTY, (x * CELL_SIZE, y * CELL_SIZE))
            if maze[(x, y)] == ENDPOINT:
                screen.blit(exit_door, (x * CELL_SIZE, y * CELL_SIZE)) 
            

def visit(x, y):
    stack = [(x, y)]
    maze[(x, y)] = PATH
    while len(stack) > 0:
        x, y = stack[-1] 
        unvisitedNeighbors = []
        if y > 1 and (x, y - 2) not in hasVisited:
            unvisitedNeighbors.append(NORTH)
        if y < MAZE_HEIGHT - 2 and (x, y + 2) not in hasVisited:
            unvisitedNeighbors.append(SOUTH)
        if x > 1 and (x - 2, y) not in hasVisited:
            unvisitedNeighbors.append(WEST)
        if x < MAZE_WIDTH - 2 and (x + 2, y) not in hasVisited:
            unvisitedNeighbors.append(EAST)
        if len(unvisitedNeighbors) == 0:
            stack.pop()
            return
        else:
            nextIntersection = random.choice(unvisitedNeighbors)
            if nextIntersection == NORTH:
                nextX = x
                nextY = y - 2
                maze[(x, y - 1)] = PATH 
            elif nextIntersection == SOUTH:
                nextX = x
                nextY = y + 2
                maze[(x, y + 1)] = PATH 
            elif nextIntersection == WEST:
                nextX = x - 2
                nextY = y
                maze[(x - 1, y)] = PATH 
            elif nextIntersection == EAST:
                nextX = x + 2
                nextY = y
                maze[(x + 1, y)] = PATH 
            hasVisited.append((nextX, nextY))
            stack.append((nextX, nextY))
            visit(nextX, nextY) # Recursively visit this space.
hasVisited = [(0, 0)] # Start by visiting the top-left corner.
visit(1, 1)
empty_cells = [cell for cell in maze if maze[cell] == PATH]
endpoint = random.choice(empty_cells)    
maze[endpoint] = ENDPOINT 


def button(x, y, text):
    global clicked
    btn_width = 150
    btn_height = 60
    button_base = pygame.Surface((btn_width, btn_height))
    button_base.fill(PURPLE)
    title = pygame.font.SysFont(None, 45).render(text, True, WHITE)
    button_base.blit(title, (btn_width//4, btn_height//4))
    screen.blit(button_base, (x, y))
    btn = pygame.Rect((x, y), (btn_width, btn_height))
    action = False
    mouse_pos = pygame.mouse.get_pos()
    if btn.collidepoint(mouse_pos):
        pygame.mouse.set_cursor()
        if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
            clicked = True
            action = True
        if pygame.mouse.get_pressed()[0] == 0:
            clicked = False
    return action
             

# Player class
class Player():
    
    def __init__(self):
        self.x = 1
        self.y = 1
        self.image = pygame.image.load("game_images/boy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width() // 18, 
                                             self.image.get_height() // 18))
        
    def move(self, dx, dy, maze):
        new_x = self.x + dx 
        new_y = self.y + dy 
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[(new_x, new_y)] != 1:
            self.x = new_x
            self.y = new_y
    
    def draw(self, screen):
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

# Timer Class
class Timer():

    def __init__(self, countdown_time):
        self.font = pygame.font.SysFont(None, 36)
        self.start_time = pygame.time.get_ticks()
        self.countdown_time = countdown_time # Time in seconds

    def get_time(self):
        elasped_time = pygame.time.get_ticks() - self.start_time
        remaining_time = self.countdown_time - elasped_time // 1000
        if remaining_time < 0:
            remaining_time = 0
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        return f"Time: {minutes:02}:{seconds:02}"

    def draw(self, screen):
        time_text = self.font.render(self.get_time(), True, BLACK)
        screen.blit(time_text, (10, 600))

    def is_time_up(self):
        elasped_time = pygame.time.get_ticks()- self.start_time
        remaining_time = self.countdown_time - elasped_time // 1000
        return remaining_time <= 0 

player = Player()
timer = Timer(countdown_time=120)
running = True
won = False
clock = pygame.time.Clock()
game_end = False

def initialize_game():
    global player
    global timer
    global clock
    global running
    global won
    maze = {}
    for x in range(MAZE_WIDTH):
        for y in range(MAZE_HEIGHT):
            maze[(x, y)] = 1 
    player = Player()
    timer = Timer(countdown_time=120)
    clock = pygame.time.Clock()
    draw_maze(maze)
    pygame.display.flip()
    return


def game_loop():
    global player
    global timer
    global running
    global won
    pygame.display.set_caption("Escape the Maze")
    img = pygame.image.load("game_images/wood_floor.jpg").convert()
    flooring = pygame.transform.scale(img, 
                                     (img.get_width() // 10, 
                                      img.get_height() // 10))
    initialize_game()
    while running:
        player.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                    player.move(0, -1, maze)
            elif keys[pygame.K_DOWN]:
                    player.move(0, 1, maze)
            elif keys[pygame.K_LEFT]:
                    player.move(-1, 0, maze)
            elif keys[pygame.K_RIGHT]:
                    player.move(1, 0, maze)
        for x in range(0, SCREEN_WIDTH, flooring.get_width()):
            for y in range(0, SCREEN_HEIGHT, flooring.get_height()):
                screen.blit(flooring, (x, y))
        draw_maze(maze)
        player.draw(screen)
        pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        timer.draw(screen)
        if maze[(player.x, player.y)] == ENDPOINT:
            won = True
            running = False
        if timer.is_time_up():
            running = False
        pygame.display.flip()
        clock.tick(30)
    return


def reset_game():
    global running
    global won
    global game_end
    running = True
    won = False
    game_end = False
    game_loop()
    return


def main():
    global player
    global timer
    global running
    global won
    global game_end
    game_over = pygame.image.load("game_images/GameOver.png").convert()
    winner = pygame.image.load("game_images/Escaped.png").convert()
    game_loop()
    while True:    
        while game_end == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True     
            if won and game_end == False:
                screen.blit(winner, (0, 0))
            elif not won and game_end == False:
                screen.blit(game_over, (0, 0))
            if button(100, 570, "Again") and game_end == False:
                game_end = True
                screen.fill(WHITE)
                reset_game()
            if button(350, 570, "Quit!") and game_end == False:
                game_end = True
                pygame.quit()
                break
            pygame.display.update()
        break
        

if __name__ == "__main__":
    main()