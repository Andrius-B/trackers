from trackers.redispatcher import configure_receiver
from contextlib import AbstractContextManager

class RedispatcherWithCleanup(AbstractContextManager):
    def __init__(self) -> None:
        self.closed = False
        self.started = False

    def __enter__(self):
         self.started = True
    
    def __exit__(self, *args, **kwargs):
         self.closed = True

def test_configure_receiver():
    redispatcher = RedispatcherWithCleanup()
    assert redispatcher.started == False
    assert redispatcher.closed == False

    with configure_receiver(redispatcher):
        assert redispatcher.started == True
        assert redispatcher.closed == False
    
    assert redispatcher.started == True
    assert redispatcher.closed == True
