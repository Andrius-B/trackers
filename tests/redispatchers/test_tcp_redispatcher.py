from trackers.dispatchers.tcp_dispatcher import TCPDispatcher
from trackers.redispatchers.tcp_redispatcher import TCPRedispatcher
from trackers.dispatcher import configure_dispatcher
from trackers.redispatcher import configure_redispatcher
from tests.test_fixtures import MockDispatcher
import trackers

TEST_PORT = 3148


def test_tcp_redispatcher():
    mock_dispatcher = MockDispatcher()
    with configure_redispatcher(TCPRedispatcher(mock_dispatcher, TEST_PORT)):
        with configure_dispatcher(TCPDispatcher(port=TEST_PORT)):
            trackers.gauge("name", "cat", 1)
    assert len(mock_dispatcher.calls) == 1
