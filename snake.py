import pygame
from collections import deque
from random import randint


class Snake:
    def __init__(self):
        self.initialize()
        self.main_loop()

    def initialize(self):
        pygame.init()

        self.scale = 25
        self.height = 25
        self.width = 25
        self.fps = 120
        self.screen_refresh_rate = 7
        self.direction = 1
        self.previous_direction = 1
        self.pixel_size = (self.scale - 2, self.scale - 2)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.is_start_screen = True
        self.gameover = False
        self.score = 0
        self.game_font = pygame.font.SysFont("Arial", 20)

        self.empty_grid = []
        for x in range(self.width):
            for y in range(self.height):
                self.empty_grid.append((x, y))

        self.snake = deque([(self.width // 2, self.height // 2)])
        self.empty_grid.remove((self.width // 2, self.height // 2))

        self.fruit_location = (self.width // 2 + 5, self.height // 2)

        self.screen = pygame.display.set_mode(
            (self.width * self.scale, self.height * self.scale))

        pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()

    def main_loop(self):
        counter = 0
        while (True):
            self.check_event()
            if counter % (self.fps // self.screen_refresh_rate) == 0:
                if not self.gameover and not self.is_start_screen:
                    self.update_snake()
                self.update_screen()
            self.clock.tick(self.fps)
            counter += 1

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.previous_direction != 2:
                    self.direction = 0
                if event.key == pygame.K_RIGHT and self.previous_direction != 3:
                    self.direction = 1
                if event.key == pygame.K_DOWN and self.previous_direction != 0:
                    self.direction = 2
                if event.key == pygame.K_LEFT and self.previous_direction != 1:
                    self.direction = 3

                if self.is_start_screen and event.key == pygame.K_SPACE:
                    self.is_start_screen = False

                if self.gameover and event.key == pygame.K_r:
                    self.initialize()

            if event.type == pygame.QUIT:
                quit()

    def update_screen(self):
        self.screen.fill((0, 0, 0))

        for x, y in self.snake:
            location = (x * self.scale, y * self.scale)
            self.screen.fill(self.white, pygame.Rect(
                location, self.pixel_size))

        fruit_x = self.fruit_location[0]
        fruit_y = self.fruit_location[1]
        fruit_location = (fruit_x * self.scale, fruit_y * self.scale)
        self.screen.fill(self.red, pygame.Rect(
            fruit_location, self.pixel_size))

        score = self.game_font.render(
            f"Score: {self.score}", True, (0, 0, 255))
        self.screen.blit(score, (5, 5))

        if self.is_start_screen:
            start = self.game_font.render(
                f"Press spacebar to start", True, (0, 0, 255))
            control = self.game_font.render(
                f"Use the arrow keys to change the direction of the snake", True, (0, 0, 255))
            goal = self.game_font.render(
                f"Eat red fruits to grow and don't hit the border or snake's own body", True, (0, 0, 255))
            self.screen.blit(goal, (self.width * self.scale / 2 - goal.get_width() /
                                    2, self.height * self.scale / 2 - goal.get_height() / 2 - 150))
            self.screen.blit(control, (self.width * self.scale / 2 - control.get_width() /
                                       2, self.height * self.scale / 2 - control.get_height() / 2 - 100))
            self.screen.blit(start, (self.width * self.scale / 2 - start.get_width() /
                                     2, self.height * self.scale / 2 - start.get_height() / 2 - 50))

        if self.gameover:
            gameover = self.game_font.render(
                f"Gameover", True, (0, 0, 255))
            restart = self.game_font.render(
                f"Press r to restart", True, (0, 0, 255))
            self.screen.blit(gameover, (self.width * self.scale / 2 - gameover.get_width() /
                                        2, self.height * self.scale / 2 - gameover.get_height() / 2))
            self.screen.blit(restart, (self.width * self.scale / 2 - restart.get_width() /
                                       2, self.height * self.scale / 2 - restart.get_height() / 2 + 25))

        pygame.display.flip()

    def update_snake(self):
        self.previous_direction = self.direction

        head_x = self.snake[-1][0]
        head_y = self.snake[-1][1]

        if self.direction == 0:
            head_y -= 1
        elif self.direction == 1:
            head_x += 1
        elif self.direction == 2:
            head_y += 1
        elif self.direction == 3:
            head_x -= 1

        if self.check_snake_collision(head_x, head_y):
            self.gameover = True
            return

        self.snake.append((head_x, head_y))
        self.empty_grid.remove((head_x, head_y))

        if ((head_x, head_y) != self.fruit_location):
            self.empty_grid.append(self.snake.popleft())
        else:
            self.score += 1
            self.spawn_fruit()

    def check_snake_collision(self, x: int, y: int):
        if (x < 0 or x >= self.width or y < 0 or y >= self.height):
            return True

        if ((x, y) in self.snake):
            return True

        return False

    def spawn_fruit(self):
        self.fruit_location = self.empty_grid[randint(
            0, len(self.empty_grid) - 1)]


if __name__ == "__main__":
    Snake()
