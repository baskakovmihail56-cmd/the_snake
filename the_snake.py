from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, position, body_color=None):
        self.position = position
        self.body_color = body_color
        
    def draw(self):
        pass


class Apple(GameObject):
    """
    Класс, представляющий яблоко в игре.
    Наследуется от GameObject.
    """
    def __init__(self, position, body_color):
        """
        Инициализирует яблоко и сразу задает ему случайную позицию.
        
        :param position: Начальная позиция (используется как заглушка, затем перезаписывается).
        :param body_color: Цвет яблока.
        """
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self):
        """
        Устанавливает случайную позицию яблока в пределах игрового поля,
        выровненную по сетке.
        """
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """
        Отрисовывает яблоко на игровом поле в виде квадрата с границей.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self, position, body_color):

        super().__init__(position, body_color)
        self.length = 1
        self.positions = [position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        return self.positions[0]
    
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        """
        берем координаты первого элемента списка self.positions 
        (это голова). Также мы берем текущее направление 
        (direction), которое является кортежем,
        """
        x, y = self.get_head_position()
        dx, dy = self.direction
        
        # Вычисляем новую позицию с учетом прохода сквозь стены (операция %)
        new_position = (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        
        # Проверка на столкновение с собой (проверяем начиная с 3-го сегмента, так как шея не может быть головой)
        if len(self.positions) > 2 and new_position in self.positions[2:]:
            self.reset()
        else:
            # Добавляем новую голову в начало списка
            self.positions.insert(0, new_position)
            
            # Если длина списка превысила разрешенную длину змейки, удаляем хвост
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                # Если змейка только что съела яблоко, хвост не удаляется
                self.last = None




    def reset(self):
        """
        Сбрасывает змейку в начальное состояние (длина 1, центр экрана, случайное направление).
        """
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self):
        """
        Отрисовывает змейку на игровом поле и затирает след от последнего сегмента.
        """
        # Отрисовка всех текущих сегментов змейки
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        
        # Затирание старого хвоста, если он был удален при движении
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)





def handle_keys(game_object):
    """
    Обрабатывает события клавиатуры для изменения направления движения змейки.
    Запрещает движение в противоположном направлении (например, вниз, если движемся вверх).
    
    :param game_object: Экземпляр класса Snake, которым управляет игрок.
    """
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
    """
    Основная функция игры, содержащая главный игровой цикл.
    """
    start_position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    snake = Snake(start_position, SNAKE_COLOR)
    apple = Apple(start_position, APPLE_COLOR)
    
    while True:
        # Ограничиваем частоту кадров, чтобы змейка не летала слишком быстро
        clock.tick(SPEED)
        
        # 1. Обработка ввода
        handle_keys(snake)
        
        # 2. Обновление состояния
        snake.update_direction()
        snake.move()
        
        # 3. Проверка поедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            
        # 4. Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана перед новой отрисовкой
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()








# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
#GHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
