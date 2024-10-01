from my_queue import MyQueue
from my_pair import MyPair
from copy import deepcopy as copy

class MySnake:
    __available_directions: tuple = ("up", "down", "left", "right")
    __segments: MyQueue[MyPair] = None

    # сегменты змейки передаются, начиная с хвоста
    def __init__(self, segments: list[MyPair]) -> None:
        self.__set_default__()

        # заполняем змейку с хвоста
        for i in range(len(segments)):
            self.__segments.add(copy(segments[i]))

    def __set_default__(self) -> None:
        self.__direction = "down"
        self.__segments = MyQueue[MyPair]()

    def grow(self) -> None:
        '''Рост змейки на 1'''
        next = self.__make_next__()
        self.__segments.add(next)

    def move(self) -> None:
        '''Двигает змейку на 1'''
        next = self.__make_next__()
        self.__segments.add(next)
        self.__segments.get()

    def __make_next__(self) -> MyPair:
        '''Ищет следующую позицию для головы '''
        next = self.__segments.peek_end()

        if self.__direction == "up":
            next.y = next.y - 1
        elif self.__direction == "down":
            next.y = next.y + 1
        elif self.__direction == "left":
            next.x = next.x - 1
        elif self.__direction == "right":
            next.x = next.x + 1

        return next

    def is_cover(self, coords: MyPair) -> bool:
        '''Проверяет: перекрывает ли змейка координаты'''
        for i in range(self.__segments.len()):
            if self.__segments.peek_by_id(i).is_equal(coords):
                return True
        return False 

    def is_body_cover(self, coords: MyPair) -> bool:
        '''Проверяет: перекрывает ли тело координаты'''
        for i in range(self.__segments.len() - 1):
            if self.__segments.peek_by_id(i).is_equal(coords):
                return True
        return False 

    def up(self) -> bool:
        '''Поворачивает голову змейки вверх; вернет True, если нужно увеличить скорость'''
        if self.__direction == "up":
            return True
        if self.__direction == "left" or self.__direction == "right":
            self.__direction = "up"
        return False
    
    def down(self) -> bool:
        '''Поворачивает голову змейки вниз; вернет True, если нужно увеличить скорость'''
        if self.__direction == "down":
            return True
        if self.__direction == "left" or self.__direction == "right":
            self.__direction = "down"
        return False
    
    def left(self) -> bool:
        '''Поворачивает голову змейки налево; вернет True, если нужно увеличить скорость'''
        if self.__direction == "left":
            return True
        if self.__direction == "up" or self.__direction == "down":
            self.__direction = "left"
        return False
    
    def right(self) -> bool:
        '''Поворачивает голову змейки направо; вернет True, если нужно увеличить скорость'''
        if self.__direction == "right":
            return True
        if self.__direction == "up" or self.__direction == "down":
            self.__direction = "right"
        return False
        
    def head(self) -> MyPair:
        '''Вернет копию головы'''
        return copy(self.__segments.peek_end())