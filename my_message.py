from __future__ import annotations

class MyMessage:
    allowed_methods = ("POST", "PUT", "GET", "DELETE", None)
    __method: str
    __entity: str
    __description: str

    def __init__(self, method: str = None, entity: str = None, description: str = None) -> None:
        if method not in self.allowed_methods:
            raise Exception(f"MyMessage.__init__: Unexpected method {method}")
        self.__method = method
        self.__entity = entity
        self.__description = description

    @property
    def method(self) -> str:
        return self.__method

    @property
    def entity(self) -> str:
        return self.__entity

    @property
    def description(self) -> str:
        return self.__description
    
    def set_method(self, value: str) -> None:
        if value not in self.allowed_methods:
            raise Exception(f"MyMessage.method(): Unexpected method {value}")
        self.__method = value
    
    def set_entity(self, value: str) -> None:
        self.__entity = value
    
    def set_description(self, value: str) -> None:
        self.__description = value

    def parse(self, msg: str) -> MyMessage:
        '''Парсит строку сообщения в объект'''
        i: int = msg.find("::")
        j: int = msg.find("::", i+2)
        self.set_method(msg[:i])
        self.set_entity(msg[i+2:j])
        self.set_description(msg[j+2:])
        return self

    def stringify(self) -> str:
        '''Создает строку'''
        return f"{self.method}::{self.entity}::{self.description}"