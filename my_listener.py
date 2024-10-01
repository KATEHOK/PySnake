from my_component import MyBaseComponent
from my_message import MyMessage
from pynput.keyboard import Key, Listener
from time import sleep

class MyListener(MyBaseComponent):
    '''Класс прослушивания событий управления'''
    
    # Слушает нажания клавиш и создает соответствующие события для обработки объектом Controller

    __normalize = {
        "w": "up",
        "a": "left",
        "s": "down",
        "d": "right",
        "Key.up": "up",
        "Key.left": "left",
        "Key.down": "down",
        "Key.right": "right",
        "Key.enter": "enter",
        "Key.space": "space",
        "Key.esc": "esc"
    }

    def __init__(self) -> None:
        pass

    def __set_default__(self) -> None:
        pass

    def start_component(self) -> None:
        '''Запускает бесконечный цикл ожидания управляющей команды'''

        while True:
            # print("Listener is waiting for messages...")
            # sleep(0.1)
            msg: MyMessage = self.receive_message()
            if msg:
                if msg.method == "POST" and msg.entity == "command" and msg.description == "run":
                    self.__listen()
                    self.send_message("POST", "status", "esc")

    def __listen(self) -> None:
        '''Начинает прослушку нажатий клавиш'''
        with Listener(on_press=self.__on_press, on_release=self.__on_release) as listener:
            listener.join()

    def __on_press(self, key: Key):
        '''Посылает различные сообщения в зависимости от нажатой клавиши'''
        try:
            if key.char in ('w', 'a', 's', 'd'):
                self.__direction__(self.__normalize[key.char])

        except AttributeError:
            if key in (Key.up, Key.left, Key.down, Key.right):
                self.__direction__(self.__normalize[str(key)])

            elif key in (Key.enter, Key.space, Key.esc):
                self.send_message("POST", "status", self.__normalize[str(key)])

    def __on_release(self, key: Key):
        if key == Key.esc:
            return False  # Остановка слушателя при нажатии ESC
        
    def __direction__(self, direction: str):
        '''Посылает сообщение направления'''
        self.send_message("POST", "direction", direction)


# Pressed: 'w'
# Pressed: 'a'
# Pressed: 's'
# Pressed: 'd'
# Pressed: Key.up
# Pressed: Key.left
# Pressed: Key.down
# Pressed: Key.right
# Pressed: Key.enter
# Pressed: Key.space
# Pressed: Key.esc