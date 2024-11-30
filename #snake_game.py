import pygame
import random

pygame.init()


WIDTH = 600
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  
        self.grow = False

    def move(self):
        head = self.body[0]
        

        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )
        

        if self.grow:
            self.body.insert(0, new_head)
            self.grow = False
        else:
            self.body.insert(0, new_head)
            self.body.pop()

    def grow_snake(self):
        self.grow = True

    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:]

    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(
                segment[0] * GRID_SIZE, 
                segment[1] * GRID_SIZE, 
                GRID_SIZE - 1, 
                GRID_SIZE - 1
            )
            pygame.draw.rect(surface, GREEN, rect)

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)

    def generate_position(self, snake_body):
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if pos not in snake_body:
                return pos

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE, 
            self.position[1] * GRID_SIZE, 
            GRID_SIZE - 1, 
            GRID_SIZE - 1
        )
        pygame.draw.rect(surface, RED, rect)

def main():
    snake = Snake()
    food = Food(snake.body)
    score = 0

    font = pygame.font.Font(None, 36)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        snake.move()

        if snake.body[0] == food.position:
            snake.grow_snake()
            food = Food(snake.body)
            score += 1

        if snake.check_collision():
            running = False

        screen.fill(BLACK)

        snake.draw(screen)
        food.draw(screen)

        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        clock.tick(10)  

    screen.fill(BLACK)
    game_over_text = font.render(f'Game Over! Score: {score}', True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(game_over_text, text_rect)
    pygame.display.flip()

    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()
