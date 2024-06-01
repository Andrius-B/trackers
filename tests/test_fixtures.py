from contextlib import contextmanager
from tempfile import TemporaryDirectory
from pathlib import Path


@contextmanager
def temp_file_closed():
    tmpdir = Path("test_data") / "profiles"
    tmpdir.mkdir(parents=True, exist_ok=True)
    file = tmpdir / "file"
    file.write_bytes(b"sample")
    yield file
    file.unlink()
    tmpdir.rmdir()
