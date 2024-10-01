from my_component import MyBaseComponent
from my_message import MyMessage
from my_pair import MyPair
from my_snake import MySnake
from random import randint
from time import sleep

# Класс игровой логики
class MyGame(MyBaseComponent):
    __field: MyPair = None
    __snake: MySnake = None
    # __process: Process = None

    # Управляется из Controller
    # Учитывая игровую логику, создает события игры для Controller

    def __init__(
            self,
            field_len: int = 50,
            field_height: int = 50,
            snake_len: int = 3,
            speed: int = 1,
            ) -> None:
        
        if field_len <= 0 or field_height <= 0:
            raise Exception("Game.__init__: Field params must be positive")
        if snake_len <= 0:
            raise Exception("Game.__init__: Snake len must be positive")
        if snake_len >= field_height:
            raise Exception("Game.__init__: Snake len must be lower then field height")
        if speed <= 0:
            raise Exception("Game.__init__: Speed must be positive")

        self.__field = MyPair(field_len, field_height)
        self.__snake_len = snake_len
        self.__default_speed = speed
        self.__set_default__()

    def __set_default__(self) -> None:
        self.__is_started = False
        self.__is_playing = False
        self.__is_attached = False
        self.__score = 0
        self.__speed = self.__default_speed

        snake: list[MyPair] = []
        for i in range(self.__snake_len):
            snake.append(MyPair(0, i))            
        self.__snake = MySnake(snake)

        self.__apple = self.__make_apple__()
        self.__is_ready_to_start = True

    def start_component(self) -> None:
        '''Запускает бесконечный цикл ожидания управляющих команд'''
        while True:
            msg: MyMessage = self.receive_message()
            if msg:
                if msg.method == "POST":
                    # изменение направления
                    if msg.entity == "direction":
                        self.__manage_direction__(msg.entity)
                    # изменение статуса игры
                    elif msg.entity == "status":
                        self.__manage_status__(msg.entity)

    def __manage_direction__(self, direction: str) -> None:
        '''Реагирует на событие направления'''
        if direction == "up":
            self.up()
        elif direction == "down":
            self.down()
        elif direction == "left":
            self.left()
        elif direction == "right":
            self.right()

    def __manage_status__(self, status: str) -> None:
        '''Реагирует на событие изменения статуса'''
        # пауза
        if status == "space":
            if self.__is_playing:
                self.pause()
            elif self.__is_started:
                self.play()
        # запуск/остановка/перезагрузка
        elif status == "enter":
            if self.__is_playing:
                self.stop()
            elif self.__is_ready_to_start:
                self.start()
            else:
                self.reload()

    def start(self) -> None:
        '''Стартует игру '''
        if not self.__is_ready_to_start:
            return
        self.__is_ready_to_start = False
        self.__is_started = True
        self.play()
    
    def stop(self) -> None:
        '''Останавливает игру'''
        self.pause()
        self.__is_started = False

    def play(self) -> None:
        '''Запускает игру'''
        if not self.__is_started or self.__is_playing:
            return
        self.__is_playing = True

    def pause(self) -> None:
        '''Приостанавливает игру'''
        if not self.__is_started or not self.__is_playing:
            return
        self.__is_playing = False

    def load(self) -> None:
        '''Подготавливает игру к старту'''
        self.__set_default__()
        self.__attach_ui__()

    def reload(self) -> None:
        '''Ломает текущую игру и подготавливает новую к старту'''
        self.__crash__()
        self.load()

    def up(self) -> None:
        '''Поворачивает змейку вверх'''
        if not self.__is_playing:
            return
        if self.__snake.up():
            self.__speed_up__()
            
    def down(self) -> None:
        '''Поворачивает змейку вниз'''
        if not self.__is_playing:
            return
        if self.__snake.down():
            self.__speed_up__()
            
    def left(self) -> None:
        '''Поворачивает змейку налево'''
        if not self.__is_playing:
            return
        if self.__snake.left():
            self.__speed_up__()
            
    def right(self) -> None:
        '''Поворачивает змейку направо'''
        if not self.__is_playing:
            return
        if self.__snake.right():
            self.__speed_up__()

    def __game_loop__(self) -> None:
        '''Игровой цикл | Запускать асинхронно'''
        while self.__is_playing:
            self.__event_move__()
            if self.__is_crash__():
                self.__crash__()
            elif self.__is_eat_apple__():
                self.__event_eat_apple__()
            sleep(1 / self.__speed)

    def __crash__(self) -> None:
        '''Ломает текущую игру'''
        self.stop()
        self.__detach_ui__()

    def __is_crash__(self) -> bool:
        '''Проверяет: сломана ли игра за последний ход'''
        if not self.__is_playing:
            return False
        head = self.__snake.head()
        return (head.x < 0 or head.x >= self.__field.x) or (head.y < 0 or head.y >= self.__field.y) or self.__snake.is_body_cover(head)

    def __is_eat_apple__(self) -> bool:
        '''Проверяет: было ли съедено яблоко за последнее движение'''
        if not self.__is_playing:
            return False
        return self.__snake.head().is_equal(self.__apple)

    def __event_move__(self) -> None:
        '''Обрабатывает событие движения'''
        self.__snake.move()
        if self.__is_crash__():
            self.__crash__()

    def __event_eat_apple__(self) -> None:
        '''Обрабатывает событие "съедено яблоко"'''
        self.__snake.grow()
        self.__speed_up__()
        self.__apple = self.__make_apple__()

    def __speed_up__(self) -> None:
        '''Увеличивает скорость на 1'''
        self.__speed += 1

    def __attach_ui__(self) -> None:
        '''Связывает логику с отрисовкой'''
        self.__is_attached = True

    def __detach_ui__(self) -> None:
        '''Отвязывает логику от отрисовки'''
        self.__is_attached = False

    def __make_apple__(self) -> MyPair:
        '''Генерирует рандомные валидные координаты для яблока'''
        apple = MyPair(randint(0, self.__field.x - 1), randint(0, self.__field.y - 1))
        while self.__snake.is_cover(apple):
            apple = MyPair(randint(0, self.__field.x - 1), randint(0, self.__field.y - 1))
        return apple