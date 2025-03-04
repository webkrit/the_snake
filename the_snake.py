"""Дорогой ревьюер, не суди строго, я только учусь и очень стараюсь (ง' -' )ง
Это моя первая игра(после крестиков-ноликов) - >Голодный Питон< (Она же Змейка)
Помни: >Ты — то, что ты ешь.< Фейербах.
"""
from random import randint

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
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Голодный Питон')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс GameObject.

    Атрибуты:
        position: Позиция объекта в двумерном пространстве, заданная кортежем
            из координат (x, y). По умолчанию объект инициализируется
            в центре экрана.
        body_color: Цвет тела объекта. По умолчанию None.

    Методы:
        draw(): Отображает объект на экране. В текущей реализации метод
        не реализован и должен быть переопределен в подклассах.
    """

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отображает объект на экране"""


class Apple(GameObject):
    """
    Класс Apple, представляющий яблоко в игре. Наследуется от класса
    GameObject и отвечает за создание, позиционирование, отображение
    и характеристику яблока.

    Атрибуты:
        body_color: Цвет яблока, назначенный константой APPLE_COLOR.
        position: Текущая позиция яблока на игровом поле.

    Методы:
        __init__(): Инициализирует яблоко и устанавливает его цвет.
        randomize_position(): Генерирует случайные координаты для яблока
            в пределах игрового поля, основываясь на заданной сетке.
        draw(): Отображает яблоко на экране, отображая его цвет и границу.
    """

    def __init__(self, occupied_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.occupied_positions = (
            occupied_positions if occupied_positions is not None else []
        )  # Занятые позии, создаем новый список если None
        self.randomize_position()

    def randomize_position(self):
        """Генерирует случайные координаты для яблока, избегая занятых"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in self.occupied_positions:
                return self.position

    def draw(self):
        """Отображает яблоко на экране, отображая его цвет и границу."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, представляющий змейку в игре Голодный Питон.

    Атрибуты:
        length: Длина змейки, представляет количество сегментов.
        positions: Список координат сегментов змейки, первый элемент - голова.
        direction: Текующее направление движения змейки, заданное кортежем.
        next_direction: Запланированное направление движения, если оно существ.
        body_color: Цвет тела змейки.

    Методы:
        update_direction(): Обновляет текущее направление движения змейки,
            устанавливая его на следующее, если оно задано.
        move(): Обновляет позиции сегментов змейки, перемещая голову и
            изменяя место положения остальных сегментов.
        get_head_position(): Возвращает координаты головы змейки.
        reset(): Сбрасывает змейку к начальному состоянию.
        draw(): Рисует змейку на экране, отображая каждый сегмент тела.
    """

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Обновляет текущее направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позиции сегментов змейки"""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction  # распаковка направлений
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        """Возвращает координаты головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку к начальному состоянию"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self):
        """Рисует змейку на экране"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
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
    Главная функция игры "Голодный Питон".

    Эта функция инициализирует игровое окно с помощью модуля PyGame. Она
    запускает главный цикл, который выполняет следующие задачи:

    1. Инициализация PyGame и создание необходимых объектов (яблоко и змейка).
    2. Очистка экрана на каждом кадре.
    3. Обработка нажатий клавиш для управления движением змейки.
    4. Обновление направления и движения змейки.
    5. Проверка условий победы и сброса игры.
    6. Отрисовка змейки и яблока на экране.
    7. Обновление дисплея для отображения изменений.

    Основной игровой цикл выполняется до тех пор, пока игра активна.
    В каждой итерации проверяются условия для увеличения длины змейки и сброса
    игры(сталкиваение с собственным телом).
    """
    pygame.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана

        handle_keys(snake)  # Обработка нажатий клавиш
        snake.update_direction()  # Обновление направления
        snake.move()  # Движение змейки

        # Проверка, съела ли змейка яблоко, логика: если голова змейки
        # совпадает с позицией яблока (apple.position), увеличивается длина
        # змейки на 1 и перемещается яблоко на новую случайную позицию.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка столкновения змейки с собой
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        apple.draw()  # Отрисовка яблока
        snake.draw()  # Отрисовка змейки

        pygame.display.update()


if __name__ == '__main__':
    main()
