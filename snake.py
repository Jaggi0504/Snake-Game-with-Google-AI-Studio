import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_COLOR = (0, 255, 0)  # Green
FOOD_COLOR = (255, 0, 0)  # Red
OBSTACLE_COLOR = (100, 100, 100)  # Gray
BACKGROUND_COLOR = (0, 0, 0)  # Black
TEXT_COLOR = (255, 255, 255)  # White

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Obstacles")

# Clock for controlling game speed
clock = pygame.time.Clock()

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Start in the middle
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction  # allows instant direction change
        self.grow = True

    def move(self, obstacles):
        head = self.body[0]
        new_head = (head[0] + self.next_direction[0], head[1] + self.next_direction[1])

        # Check for collision with walls
        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        ):
            return False  # Game over

        # Check for collision with itself
        if new_head in self.body[1:]:
            return False  # Game over

        # Check for collision with obstacles
        if new_head in obstacles:
            return False

        self.body.insert(0, new_head)  # Add new head

        if not self.grow:
            self.body.pop()  # Remove tail if not growing
        else:
            self.grow = False

        self.direction = self.next_direction  # update to next intended direction
        return True  # Game continues

    def render(self, screen):
        for segment in self.body:
            pygame.draw.rect(
                screen, SNAKE_COLOR, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )


# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def randomize_position(self, snake_body, obstacles):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_body and self.position not in obstacles:  # Ensure food doesn't spawn on snake or obstacles
                break

    def render(self, screen):
        pygame.draw.rect(
            screen, FOOD_COLOR, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )


# Obstacle class
class Obstacle:
    def __init__(self, num_obstacles):
        self.obstacles = []
        self.generate_obstacles(num_obstacles)

    def generate_obstacles(self, num_obstacles):
        for _ in range(num_obstacles):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                if (x, y) not in self.obstacles:
                    self.obstacles.append((x, y))
                    break

    def render(self, screen):
        for obstacle in self.obstacles:
            pygame.draw.rect(
                screen, OBSTACLE_COLOR, (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )

    def get_obstacles(self):
        return self.obstacles

# Game Over function
def game_over_screen(screen, score):
    font = pygame.font.Font(None, 50)
    game_over_text = font.render("Game Over", True, TEXT_COLOR)
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    restart_text = font.render("Press SPACE to restart or ESC to quit", True, TEXT_COLOR)

    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # Restart the game
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    return False


# Main game function
def main():
    snake = Snake()
    food = Food()
    num_obstacles = 10  # Adjust the number of obstacles
    obstacle = Obstacle(num_obstacles)
    obstacles = obstacle.get_obstacles()

    food.randomize_position(snake.body, obstacles)
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT

        if not game_over:
            if not snake.move(obstacles):
                game_over = True

            if snake.body[0] == food.position:
                snake.grow = True
                food.randomize_position(snake.body, obstacles)
                score += 1

            # Clear the screen
            screen.fill(BACKGROUND_COLOR)

            # Render the snake, food and obstacles
            snake.render(screen)
            food.render(screen)
            obstacle.render(screen)

            # Display the score
            font = pygame.font.Font(None, 30)
            score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(score_text, (5, 5))

            # Update the display
            pygame.display.flip()

            # Control the game speed
            clock.tick(10)
        else:
            # Game over screen
            restart = game_over_screen(screen, score)
            if restart:
                main()  # Restart the game
                return  # Important to exit current instance of main() to avoid recursion
            else:
                break  # Exit the game loop

    pygame.quit()
    sys.exit()


# Run the game
if __name__ == "__main__":
    main()