from multiprocessing import Process, Queue
from my_game import MyGame
from my_listener import MyListener
from my_display import MyDisplay
from controller import Controller

from time import sleep

MAX_QUEUE_SIZE = 10

if __name__ == "__main__":
    controller = Controller()
    controller.set_components(MyGame(), MyDisplay(), MyListener())
    controller.set_queues(Queue(MAX_QUEUE_SIZE), Queue(MAX_QUEUE_SIZE), Queue(MAX_QUEUE_SIZE), Queue(MAX_QUEUE_SIZE), Queue(MAX_QUEUE_SIZE))
    controller.set_processes(
        Process(target=controller.game.start_base_component, name="game", args=(controller.into_game, controller.from_game)),
        Process(target=controller.display.start_base_component, name="display", args=(controller.into_display, None)),
        Process(target=controller.listener.start_base_component, name="listener", args=(controller.into_listener, controller.from_listener)),
    )
    controller.start_processes()
    controller.start()
    controller.stop_processes()
