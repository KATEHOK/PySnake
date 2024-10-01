from __future__ import annotations
from copy import deepcopy as copy

class MyPair:

    def __init__(self, x: int, y: int) -> None:
        self.__set_default__()
        self.__x = x
        self.__y = y

    def __set_default__(self) -> None:
        self.__x = 0
        self.__y = 0

    def is_equal(self, other: MyPair) -> bool:
        return self.__x == other.__x and self.__y == other.__y
    
    def copy(self) -> MyPair:
        return copy(self)
    
    @property
    def x(self) -> int:
        return copy(self.__x)
    
    @property
    def y(self) -> int:
        return copy(self.__y)
    
    @x.setter
    def x(self, value: int) -> None:
        self.__x = copy(value)
    
    @y.setter
    def y(self, value: int) -> None:
        self.__y = copy(value)