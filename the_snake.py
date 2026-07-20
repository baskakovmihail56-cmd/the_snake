from random import randint

import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения (векторы смещения по X и Y)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета в формате RGB
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки (кадров в секунду)
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(
        self,
        position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        body_color=None
    ):
        """Инициализирует базовый игровой объект.

        :param position: Начальная позиция объекта (x, y).
        :param body_color: Цвет объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(
        self,
        position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        body_color=APPLE_COLOR
    ):
        """Инициализирует яблоко и сразу задает ему случайную позицию.

        :param position: Начальная позиция (заглушка).
        :param body_color: Цвет яблока.
        """
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока в пределах поля."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко на игровом поле в виде квадрата с границей."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(
        self,
        position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        body_color=SNAKE_COLOR
    ):
        """Инициализирует змейку с начальными параметрами.

        :param position: Начальная позиция головы змейки.
        :param body_color: Цвет змейки.
        """
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки на следующее."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        new_position = (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовывает змейку и затирает след от хвоста."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает события клавиатуры для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    pygame.init()
    start_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    snake = Snake(start_position)
    apple = Apple(start_position)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка поедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Избегаем появления яблока внутри змейки
            while apple.position in snake.positions:
                apple.randomize_position()

        # Проверка столкновения с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
