from trackers.receiver import configure_receiver
from contextlib import AbstractContextManager

class ReceiverWithCleanup(AbstractContextManager):
    def __init__(self) -> None:
        self.closed = False
        self.started = False

    def __enter__(self):
         self.started = True
    
    def __exit__(self, *args, **kwargs):
         self.closed = True

def test_configure_receiver():
    receiver = ReceiverWithCleanup()
    assert receiver.started == False
    assert receiver.closed == False

    with configure_receiver(receiver):
        assert receiver.started == True
        assert receiver.closed == False
    
    assert receiver.started == True
    assert receiver.closed == True
