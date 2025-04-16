import random
import pygame


pygame.init()
# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650 # Increased height for timer display
CELL_SIZE = 20
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAZE_HEIGHT = (SCREEN_HEIGHT - 50) // CELL_SIZE # Adjusted height for timer display
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (192, 192, 192)

# Create Maze
def create_maze():
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
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze [y][x] == 2:
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))    


def main():
    ...



if __name__ == "__main__":
    main()