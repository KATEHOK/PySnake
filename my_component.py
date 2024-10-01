from multiprocessing import Process, Queue
from my_message import MyMessage
from my_message_agent import MyMessageAgent
from time import sleep

class MyBaseComponent(MyMessageAgent):
    '''Класс базового компонента'''

    __process: Process = None
    incomming_queue: Queue = None
    outcomming_queue: Queue = None

    def set_process(self, process: Process) -> None:
        '''Устанавливает процесс'''
        self.__process = process

    def start_process(self) -> None:
        '''Стартует процесс'''
        if not self.__process:
            raise Exception("MyBaseComponent.start_process: Process must be inited")
        self.__process.start()

    def stop_process(self) -> None:
        '''Завершает процесс'''
        if not self.__process:
            raise Exception("MyBaseComponent.stop_process: Process must be inited")
        self.__process.terminate()

    def start_base_component(self, incomming: Queue = None, outcomming: Queue = None) -> None:
        '''Устанавливает очереди, запускает компонент'''
        self.incomming_queue = incomming
        self.outcomming_queue = outcomming
        self.start_component()
    
    def start_component(self) -> None:
        '''Запускает компонент (переопределяется подклассом)'''
        pass

    def send_message(self, method: str, entity: str, description: str = None) -> None:
        '''Форматирует и добавляет в исходящую очередь сообщение (переопределяет метод класса MyMessageAgent)'''
        super().send_message(self.outcomming_queue, method, entity, description)

    def receive_message(self) -> MyMessage:
        '''Принимает (при наличии) из входящей очереди сообщение, парсит и возвращает его или None (переопределяет метод класса MyMessageAgent)'''
        return super().receive_message(self.incomming_queue)
        
