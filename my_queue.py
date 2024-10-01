from copy import deepcopy as copy

class MyQueue[T]:
    __items: list[T] = []

    def __init__(self) -> None:
        self.__set_default__()

    def __set_default__(self) -> None:
        pass

    def add(self, item: T) -> None:
        '''Добавить элемент в конец очереди'''
        self.__items.append(item)

    def get(self) -> T:
        '''Получить элемент из начала очереди (с удалением)'''
        return self.__items.pop(0)

    def peek(self) -> T:
        '''Посмотреть элемент из начала очереди'''
        return copy(self.__items[0])

    def peek_end(self) -> T:
        '''Посмотреть элемент из конца очереди'''
        return copy(self.__items[-1])

    def is_empty(self) -> bool:
        '''Проверка: пуста ли очередь'''
        return len(self.__items) == 0
     
    def peek_by_id(self, id: int) -> T:
        '''Посмотреть элемент по индексу'''
        return copy(self.__items[id])
    
    def len(self) -> int:
        '''Длина очереди'''
        return len(self.__items)