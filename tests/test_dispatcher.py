from typing import Any
from pytest import raises
from trackers.dispatcher import configure_dispatcher
from trackers.trackers import track
from trackers.json import Event

def test_default_dispatcher():
    with raises(NotImplementedError):
        with track("sample", "c"):
            pass

def test_configure_dispatcher():
        events = []
        dispatcher = lambda e: events.append(e)
        with configure_dispatcher(dispatcher):
            with track("sample", "c"):
                pass
            assert len(events) == 2
            assert events[0].ts < events[1].ts

class DispatcherWithCleanup:
    def __init__(self) -> None:
        self.closed = False

    def __call__(self, event: Event) -> Any:
         pass
    
    def __exit__(self, **kwargs):
         self.closed = True

def test_configure_dispatcher_cleanup():
        temp_dispatcher = DispatcherWithCleanup()
        with configure_dispatcher(temp_dispatcher):
            with track("sample", "c"):
                assert temp_dispatcher.closed == False
                pass
        assert temp_dispatcher.closed == True
    