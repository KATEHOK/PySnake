from my_component import MyBaseComponent
from my_message import MyMessage
from time import sleep

class MyDisplay(MyBaseComponent):
    '''Класс отрисовки компонентов игры'''

    # Отрисовывает окна в зависимости от управляющих сообщений Controller

    def __init__(self) -> None:
        pass

    def __set_default__(self) -> None:
        pass

    def start_component(self) -> None:
        '''Запускает бесконечный цикл ожидания управляющих команд'''
        while True:
            # print("Display is waiting for messages...")
            # sleep(0.01)
            msg: MyMessage = self.receive_message()
            if msg:
                print(msg.stringify())
