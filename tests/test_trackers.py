import trackers.dispatcher
from trackers.json import Event
from tests.test_fixtures import MockDispatcher
import trackers.trackers as t


def mock_dispatcher(mocker) -> list[Event]:
    mock = MockDispatcher()
    mocker.patch.object(trackers.dispatcher, "_dispatcher", mock)
    return mock.calls


def test_tracked(mocker):
    dispatched_events = mock_dispatcher(mocker)
    with t.tracked("name", "cat"):
        pass
    assert len(dispatched_events) == 2
    assert all(d.name == "name" for d in dispatched_events)
    assert all(d.cat == "cat" for d in dispatched_events)
    assert dispatched_events[1].args is None


def test_gauge(mocker):
    dispatched_events = mock_dispatcher(mocker)
    t.gauge("name", "cat", 1)
    assert len(dispatched_events) == 1
    assert dispatched_events[0].name == "name"
    assert dispatched_events[0].cat == "cat"
    assert dispatched_events[0].ph.name == "C"
    assert dispatched_events[0].args["value"] == 1
