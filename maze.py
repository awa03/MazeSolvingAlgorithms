import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
WHITE, BLUE, RED, BLACK, GREEN = (255, 255, 255), (0, 0, 255), (255, 0, 0), (0, 0, 0), (0, 255, 0)
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

# Function to perform DFS
def DFS():
    global maze
    if start_pos is not None and end_pos is not None:
        visited = [[False] * COLS for _ in range(ROWS)]
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        path = dfs_recursive(start_row, start_col, end_row, end_col, visited, [])
        reset_backtracked_squares(path)

def dfs_recursive(row, col, end_row, end_col, visited, path):
    if row == end_row and col == end_col:
        return path + [(row, col)]

    visited[row][col] = True
    maze[row][col] = GREEN  # Mark visited tiles as green
    draw_maze()

    pygame.display.flip()
    pygame.time.delay(100)  # Add a delay for visualization purposes

    # Define the possible moves (up, right, down, left)
    moves = [(-1, 0), (0, 1), (0, -1), (1, 0)]

    for move in moves:
        new_row, new_col = row + move[0], col + move[1]

        # Check if the new position is within the maze boundaries and not a wall or visited
        if (
            0 <= new_row < ROWS
            and 0 <= new_col < COLS
            and maze[new_row][new_col] not in {3, GREEN}
            and not visited[new_row][new_col]
        ):
            new_path = dfs_recursive(new_row, new_col, end_row, end_col, visited, path + [(row, col)])
            if new_path:
                return new_path

    return []

def reset_backtracked_squares(path):
    global maze
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == GREEN and (row, col) not in path:
                maze[row][col] = WHITE

# Create the button
button_rect = pygame.Rect(WIDTH - 100, 0, 100, 50)

def draw_button():
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("DFS", True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

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
                DFS()  # Call DFS function when the button is clicked

    # Draw the maze
    screen.fill(WHITE)
    draw_maze()

    # Draw the button
    draw_button()

    # Update the display
    pygame.display.flip()
