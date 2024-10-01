from multiprocessing import Process, Queue
from my_message import MyMessage
from my_message_agent import MyMessageAgent
from my_listener import MyListener
from my_display import MyDisplay
from my_game import MyGame
from time import sleep

class Controller(MyMessageAgent):
    '''Класс управления всеми компонентами приложения'''

    # Создает компоненты игры (MyUi и MyGame) в отдельных процессах
    # На основании событий, созданных MyUi, управляет логикой игры (вызывает функции MyGame)
    # На основании событий, созданных MyGame, управляет пользовательским интерфейсом (вызывает функции MyUi)

    def __init__(self) -> None:
        pass
        
    def __set_default__(self) -> None:
        # self.__field_len = 10
        # self.__field_height = 10
        # self.__snake_len = 3
        # self.__speed = 1
        pass

    def set_queues(self, from_game: Queue, into_game: Queue, into_display: Queue, from_listener: Queue, into_listener: Queue) -> None:
        '''Добавляет очереди межпроцессных сообщений'''
        self.from_game = from_game
        self.into_game = into_game
        self.into_display = into_display
        self.from_listener = from_listener
        self.into_listener = into_listener

    def set_components(self, game: MyGame, display: MyDisplay, listener: MyListener) -> None:
        '''Установка компонентов'''
        self.game = game
        self.display = display
        self.listener = listener

    def set_processes(self, game: Process, display: Process, listener: Process) -> None:
        '''Устанавливает процессы компонентов'''
        self.game.set_process(game)
        self.display.set_process(display)
        self.listener.set_process(listener)

    def start_processes(self) -> None:
        '''Запуск процессов'''
        self.game.start_process()
        self.display.start_process()
        self.listener.start_process()

    def stop_processes(self) -> None:
        '''Завершает запущенные процессы'''
        self.game.stop_process()
        self.display.stop_process()
        self.listener.stop_process()
    
    def __received_from_game__(self, msg: MyMessage) -> None:
        '''Обрабатывает сообщение от игры'''
        pass
        
    def __received_from_listener__(self, msg: MyMessage) -> None:
        '''Обрабатывает сообщение от слушателя клавиатуры'''
        if msg.method == "POST":
            if msg.entity == "status" and msg.description == "esc":
                self.__manage_esc__()

            elif msg.entity == "status" and msg.description == "enter":
                self.__manage_enter__()

            elif msg.entity == "status" and msg.description == "space":
                self.__manage_space__()
            
            elif msg.entity == "direction":
                self.__manage_direction__(msg.description)

    def __manage_direction__(self, direction: str) -> None:
        '''Обрабатывает события направлений'''
        print(f"Controller: managing direction '{direction}'")

    def __manage_enter__(self) -> None:
        '''Обрабатывает нажатие Enter'''
        print("Controller: managing status Enter")
        
    def __manage_space__(self) -> None:
        '''Обрабатывает нажатие Space'''
        print("Controller: managing status Space")
        
    def __manage_esc__(self) -> None:
        '''Обрабатывает нажатие Esc'''
        print("Controller: managing status Esc")
        self.__is_running = False


    def start(self) -> None:
        '''Принимает управление игрой на себя'''
        self.__is_running = True

        self.send_message(self.into_listener, "POST", "command", "run")

        while self.__is_running:
            msg: MyMessage = None

            msg = self.receive_message(self.from_game)
            if msg:
                # print("Controller: ", msg.stringify())
                self.__received_from_game__(msg)

            msg = self.receive_message(self.from_listener)
            if msg:
                # print("Controller: ", msg.stringify())
                self.__received_from_listener__(msg)
