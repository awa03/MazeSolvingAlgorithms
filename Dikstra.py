import pygame
import sys
import heapq
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
WHITE, BLUE, RED, BLACK, GREEN, PURPLE = (255, 255, 255), (0, 0, 255), (255, 0, 0), (0, 0, 0), (0, 255, 0), (128, 0, 128)
BUTTON_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Drawer")

# Initialize maze array
maze = [[0] * COLS for _ in range(ROWS)]

# Start and end positions
start_pos = None
end_pos = None

# Function to perform Dijkstra's shortest path
def dijkstra():
    global maze
    if start_pos is not None and end_pos is not None:
        visited = [[False] * COLS for _ in range(ROWS)]
        distances = [[float('inf')] * COLS for _ in range(ROWS)]
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Priority queue to store cells and their distances
        pq = [(0, start_row, start_col)]
        heapq.heapify(pq)

        distances[start_row][start_col] = 0

        # Timer to control visualization delay
        pygame.time.set_timer(pygame.USEREVENT, 100)

        while pq:
            current_dist, current_row, current_col = heapq.heappop(pq)

            if visited[current_row][current_col]:
                continue

            visited[current_row][current_col] = True

            # Define the possible moves (up, down, left, right)
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for move in moves:
                new_row, new_col = current_row + move[0], current_col + move[1]

                # Check if the new position is within the maze boundaries and not a wall or visited
                if (
                    0 <= new_row < ROWS
                    and 0 <= new_col < COLS
                    and maze[new_row][new_col] not in {3}
                    and not visited[new_row][new_col]
                ):
                    new_dist = current_dist + 1  # Assuming each move has a cost of 1

                    if new_dist < distances[new_row][new_col]:
                        distances[new_row][new_col] = new_dist
                        heapq.heappush(pq, (new_dist, new_row, new_col))

                    # Mark the cell as visited for visualization
                    maze[new_row][new_col] = GREEN

                    # Draw the maze and update the display
                    draw_maze()
                    pygame.display.flip()

            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.USEREVENT:
                    # Reset the timer for the next iteration
                    pygame.time.set_timer(pygame.USEREVENT, 0)

        # Mark the shortest path
        row, col = end_row, end_col
        while (row, col) != start_pos:
            maze[row][col] = PURPLE

            # Draw the maze and update the display
            draw_maze()
            pygame.display.flip()

            # Find the previous cell with the minimum distance
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            min_dist = float('inf')
            next_row, next_col = row, col  # Initialize next_row and next_col

            for move in moves:
                new_row, new_col = row + move[0], col + move[1]

                if (
                    0 <= new_row < ROWS
                    and 0 <= new_col < COLS
                    and distances[new_row][new_col] < min_dist
                ):
                    min_dist = distances[new_row][new_col]
                    next_row, next_col = new_row, new_col

            row, col = next_row, next_col  # Update row and col for the next iteration

            # Draw the maze and update the display
            draw_maze()
            pygame.display.flip()

        # Reset the maze colors after the algorithm is complete
        reset_maze_colors()

# Function to reset the maze colors
def reset_maze_colors():
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == GREEN:
                maze[row][col] = WHITE
            

# Function to generate a random maze
def generate_random_maze():
    global maze, start_pos, end_pos
    maze = [[0] * COLS for _ in range(ROWS)]

    # Place random walls
    for _ in range(int(0.2 * ROWS * COLS)):  # Adjust the density of walls as needed
        row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        if maze[row][col] not in {1, 2}:
            maze[row][col] = 3  # Set maze wall

    # Set a random start point
    start_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    maze[start_pos[0]][start_pos[1]] = 1

    # Set a random end point, ensuring it is reachable
    while True:
        end_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if maze[end_pos[0]][end_pos[1]] not in {1, 3}:  # Ensure end point is not on start or a wall
            break

# Create the button for Dijkstra's algorithm
button_rect = pygame.Rect(WIDTH - 200, 0, 200, 50)

def draw_button():
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    font = pygame.font.Font(None, 16)
    text = font.render("Dijkstra's Shortest Path", True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

# Create the button for random maze generation
random_maze_button_rect = pygame.Rect(WIDTH - 400, 0, 200, 50)

def draw_random_maze_button():
    pygame.draw.rect(screen, BUTTON_COLOR, random_maze_button_rect)
    font = pygame.font.Font(None, 16)
    text = font.render("Generate Random Maze", True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=random_maze_button_rect.center)
    screen.blit(text, text_rect)

# Function to draw the maze
def draw_maze():
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == 2:
                pygame.draw.rect(screen, RED, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == 3:
                pygame.draw.rect(screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == GREEN:
                pygame.draw.rect(screen, GREEN, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == PURPLE:
                pygame.draw.rect(screen, PURPLE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Main game loop
current_setting = 1  # 1 for start, 2 for end, 3 for wall, 4 for erase
dragging = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            clicked_row, clicked_col = mouseY // GRID_SIZE, mouseX // GRID_SIZE

            if current_setting == 1:
                maze[clicked_row][clicked_col] = 1  # Set start point
                start_pos = (clicked_row, clicked_col)
                current_setting = 2  # Switch to end point
            elif current_setting == 2:
                maze[clicked_row][clicked_col] = 2  # Set end point
                end_pos = (clicked_row, clicked_col)
                current_setting = 3  # Switch to wall
            elif current_setting == 3:
                if maze[clicked_row][clicked_col] not in {1, 2}:  # Prevent placing walls on start/end points
                    maze[clicked_row][clicked_col] = 3  # Set maze wall
                dragging = True
            elif current_setting == 4:
                if maze[clicked_row][clicked_col] == 3:  # If it's a wall, remove it
                    maze[clicked_row][clicked_col] = WHITE
                elif maze[clicked_row][clicked_col] == 1:  # If it's the start point, remove it
                    maze[clicked_row][clicked_col] = WHITE
                    start_pos = None
                elif maze[clicked_row][clicked_col] == 2:  # If it's the end point, remove it
                    maze[clicked_row][clicked_col] = WHITE
                    end_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging and (current_setting == 3 or current_setting == 4):
                mouseX, mouseY = pygame.mouse.get_pos()
                dragged_row, dragged_col = mouseY // GRID_SIZE, mouseX // GRID_SIZE
                if maze[dragged_row][dragged_col] not in {1, 2}:  # Prevent placing/removing on start/end points
                    if current_setting == 3:
                        maze[dragged_row][dragged_col] = 3  # Set maze wall
                    elif current_setting == 4:
                        maze[dragged_row][dragged_col] = WHITE  # Remove maze wall
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            if button_rect.collidepoint(event.pos):
                dijkstra()  # Call Dijkstra's algorithm when the button is clicked
            elif random_maze_button_rect.collidepoint(event.pos):
                generate_random_maze()  # Call random maze generation when the button is clicked

    # Draw the maze
    screen.fill(WHITE)
    draw_maze()

    # Draw the buttons
    draw_button()
    draw_random_maze_button()

    # Update the display
    pygame.display.flip()
