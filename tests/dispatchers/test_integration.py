from pathlib import Path
import pytest
from trackers.dispatcher import configure_dispatcher
from trackers.redispatcher import configure_redispatcher
from trackers.dispatchers.sync_file_dispatcher import SyncFileDispatcher
from trackers.dispatchers.tcp_dispatcher import TCPDispatcher
from trackers.redispatchers.tcp_redispatcher import TCPRedispatcher
from trackers.trackers import tracked


@pytest.fixture(autouse=True)
def run_around_tests():
    Path("test_data").mkdir(parents=True, exist_ok=True)
    yield


def test_fibonacci_sync_file():
    f = Path("test_data/fibonacci.json")
    with configure_dispatcher(SyncFileDispatcher(f)):
        assert 610 == fibonacci(15)


def test_fibonacci_tcp():
    with SyncFileDispatcher(Path("test_data/fibonacci_tcp.json")) as output_dispatcher:
        with configure_redispatcher(TCPRedispatcher(output_dispatcher)):
            with configure_dispatcher(TCPDispatcher()):
                assert 610 == fibonacci(15)


def fibonacci(n: int):
    with tracked(f"{n}", "fibonacci"):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)
