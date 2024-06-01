from contextlib import contextmanager
from trackers import Event
from pathlib import Path


class MockDispatcher:
    def __init__(self) -> None:
        self.calls: list[Event] = []

    def __call__(self, e: Event):
        self.calls.append(e)


@contextmanager
def temp_file_closed():
    tmpdir = Path("test_data") / "profiles"
    tmpdir.mkdir(parents=True, exist_ok=True)
    file = tmpdir / "file"
    file.write_bytes(b"sample")
    yield file
    file.unlink()
    tmpdir.rmdir()
