from trackers.redispatcher import configure_redispatcher, Redispatcher
from trackers.dispatcher import TDispatcher
from trackers.json import Event, Phase
from tests.test_fixtures import MockDispatcher


class RedispatcherWithCleanup(Redispatcher):
    def __init__(self, base_dispatcher: TDispatcher) -> None:
        super().__init__(base_dispatcher)
        self.closed = False
        self.started = False

    def __enter__(self):
        self.started = True

    def __exit__(self, *args, **kwargs):
        self.closed = True


def test_configure_receiver():
    mock_dispatcher = MockDispatcher()
    redispatcher = RedispatcherWithCleanup(mock_dispatcher)
    assert redispatcher.started == False
    assert redispatcher.closed == False

    with configure_redispatcher(redispatcher):
        assert redispatcher.started == True
        redispatcher.redispatch(Event("sample", "sample", 1, 1, Phase.C, 1, None))
        assert redispatcher.closed == False

    assert redispatcher.started == True
    assert redispatcher.closed == True
    assert len(mock_dispatcher.calls) == 1
