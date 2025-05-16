import pygame
import random

# Иницијализација на pygame
pygame.init()

# Константи
WINDOW_SIZE = 800
GRID_SIZE = 5
CELL_SIZE = 100
MARGIN = (WINDOW_SIZE - (GRID_SIZE * CELL_SIZE)) // 2

# Бои
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0),  # црвена
    (0, 255, 0),  # зелена
    (0, 0, 255),  # сина
    (255, 255, 0)  # жолта
]

# Креирање на прозорец
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Color Fill Puzzle")


class ColorFillPuzzle:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected_color = 0

    def is_valid_move(self, row, col, color):
        # Проверка на соседните полиња
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                if self.grid[new_row][new_col] == color:
                    return False
        return True

    def draw(self, screen):
        # Црта мрежа
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = MARGIN + col * CELL_SIZE
                y = MARGIN + row * CELL_SIZE

                color = self.grid[row][col] if self.grid[row][col] is not None else WHITE
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

        # Црта палета со бои
        for i, color in enumerate(COLORS):
            pygame.draw.rect(screen, color,
                             (20 + i * 60, WINDOW_SIZE - 60, 50, 50))
            if i == self.selected_color:
                pygame.draw.rect(screen, BLACK,
                                 (20 + i * 60, WINDOW_SIZE - 60, 50, 50), 3)

    def handle_click(self, pos):
        x, y = pos

        # Проверка дали е кликнато на палетата со бои
        if WINDOW_SIZE - 60 <= y <= WINDOW_SIZE - 10:
            color_idx = (x - 20) // 60
            if 0 <= color_idx < len(COLORS):
                self.selected_color = color_idx
                return

        # Проверка дали е кликнато на мрежата
        if MARGIN <= x <= WINDOW_SIZE - MARGIN and MARGIN <= y <= WINDOW_SIZE - MARGIN:
            grid_x = (x - MARGIN) // CELL_SIZE
            grid_y = (y - MARGIN) // CELL_SIZE

            if self.is_valid_move(grid_y, grid_x, COLORS[self.selected_color]):
                self.grid[grid_y][grid_x] = COLORS[self.selected_color]

    def is_complete(self):
        # Проверка дали сите полиња се обоени
        return all(all(cell is not None for cell in row) for row in self.grid)


def main():
    game = ColorFillPuzzle()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)

                if game.is_complete():
                    print("Честитки! Успешно ја завршивте играта!")

        screen.fill(WHITE)
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()