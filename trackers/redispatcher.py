from contextlib import contextmanager, AbstractContextManager
from trackers.dispatcher import TDispatcher
from trackers.json import Event


class Redispatcher(AbstractContextManager):
    def __init__(self, dispatcher: TDispatcher) -> None:
        super().__init__()
        self.base_dispatcher = dispatcher

    def redispatch(self, e: Event):
        self.base_dispatcher(e)


@contextmanager
def configure_receiver(receiver: Redispatcher):
    with receiver:
        yield
