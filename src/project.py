import random
import pygame


pygame.init()
# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650 # Increased height for timer display
CELL_SIZE = 25
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAZE_HEIGHT = (SCREEN_HEIGHT - 50) // CELL_SIZE # Adjusted height for timer display
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (192, 192, 192)

# Create Maze
def create_maze():
    # use a maze generation algorithms and comment this off for later so that
    # can use for personal obstacles that I'll implement later that will be retractable
    maze = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
    # Randomly add obstacles
    for _ in range(200):
        x = random.randint(0, MAZE_WIDTH - 1)
        y = random.randint(0, MAZE_HEIGHT - 1)
        maze[y][x] = 1
    # Set endpoint
    maze[MAZE_HEIGHT - 1][MAZE_WIDTH - 1] = 2
    return maze

# Draw Maze
def draw_maze(screen, maze):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze [y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE,
                                                 CELL_SIZE, CELL_SIZE))
            elif maze [y][x] == 2:
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE,
                                               CELL_SIZE, CELL_SIZE))    

# Player class
class Player():
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.image.load("boy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width() // 18, 
                                            self.image.get_height() // 18))
        
    def move(self, dx, dy, maze):
        new_x = self.x + dx 
        new_y = self.y + dy 
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] != 1:
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


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("Escape the Maze")
    clock = pygame.time.Clock()
    maze = create_maze()
    image = pygame.image.load("wood_floor.jpg").convert()
    game_over = pygame.image.load("GameOver.png").convert()
    winner = pygame.image.load("Escaped.png").convert()
    flooring = pygame.transform.scale(image, 
                                            (image.get_width() // 10, 
                                             image.get_height() // 10))
    player = Player()
    countdown_time = 120 # Countdown time in seconds (2 minutes)
    timer = Timer(countdown_time)
    running = True
    won = False
    while running:
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
        screen.fill(WHITE)
        for x in range(0, SCREEN_WIDTH, flooring.get_width()):
            for y in range(0, SCREEN_HEIGHT, flooring.get_height()):
                screen.blit(flooring, (x, y))
        draw_maze(screen, maze)
        player.draw(screen)
        pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        timer.draw(screen)
        if maze[player.y][player.x] == 2:
            won = True
            running = False
        if timer.is_time_up():
            running = False
        pygame.display.flip()
        clock.tick(30)
    screen.fill(WHITE)
    if won:
        screen.blit(winner, (0, 0))
    else:
        screen.blit(game_over, (0, 0))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()


if __name__ == "__main__":
    main()