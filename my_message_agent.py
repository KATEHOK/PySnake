from multiprocessing import Queue
from my_message import MyMessage
from time import sleep

class MyMessageAgent:

    def send_message(self, target: Queue, method: str, entity: str, description: str = None) -> None:
        '''Форматирует и добавляет в целевую очередь сообщение'''
        if not target:
            raise Exception("MyMessageAgent.send_message: The target queue is not exist")
        if target.full():
            raise Exception("MyMessageAgent.send_message: The target queue is overflow")
        target.put(MyMessage(method, entity, description).stringify())

    def receive_message(self, target: Queue) -> MyMessage:
        '''Принимает (при наличии) из целевой очереди сообщение, парсит и возвращает его или False'''
        if not target:
            raise Exception("MyMessageAgent.receive_message: The target queue is not exist")
        if not target.empty():
            return MyMessage().parse(target.get())
        return None