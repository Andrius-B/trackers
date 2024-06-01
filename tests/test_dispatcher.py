from typing import Any
from pytest import raises
from trackers.dispatcher import configure_dispatcher
from trackers.trackers import tracked
from trackers.json import Event

def test_default_dispatcher():
    with raises(NotImplementedError):
        with tracked("sample", "c"):
            pass

def test_configure_dispatcher():
        events = []
        dispatcher = lambda e: events.append(e)
        with configure_dispatcher(dispatcher):
            with tracked("sample", "c"):
                pass
            assert len(events) == 2
            assert events[0].ts < events[1].ts

class DispatcherWithCleanup:
    def __init__(self) -> None:
        self.closed = False

    def __call__(self, event: Event) -> Any:
         pass
    
    def __exit__(self, *args, **kwargs):
         self.closed = True

def test_configure_dispatcher_cleanup():
        temp_dispatcher = DispatcherWithCleanup()
        with configure_dispatcher(temp_dispatcher):
            with tracked("sample", "c"):
                assert temp_dispatcher.closed == False
                pass
        assert temp_dispatcher.closed == True
    