from pathlib import Path
import pytest
from trackers.dispatcher import configure_dispatcher
from trackers.dispatchers.sync_file_dispatcher import SyncFileDispatcher
from trackers.trackers import tracked


@pytest.fixture(autouse=True)
def run_around_tests():
    Path("test_data").mkdir(parents=True, exist_ok=True)
    yield


def test_fibonacci_produce():
    f = Path("test_data/fibonacci.json")
    with configure_dispatcher(SyncFileDispatcher(f)):
        assert 610 == fibonacci(15)


# def test_fibonacci_tcp():
#     f = Path("test_data/fibonacci.json")
#     with configure_dispatcher(SyncFileDispatcher(f)):
#         assert 610 == fibonacci(15)


def fibonacci(n: int):
    with tracked(f"{n}", "fibonacci"):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)
