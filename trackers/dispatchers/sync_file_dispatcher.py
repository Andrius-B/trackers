from pathlib import Path
from trackers.json import Event
from trackers.dispatcher import TDispatcher

class SyncFileDispatcher(TDispatcher):
    def __init__(self, path: Path) -> None:
        self._fp = path
        self.writer = open(self._fp, "w")
        assert self.writer.writable(), "Output file not writable!"
        self.writer.__enter__()
        self.writer.write("[\n")
        self.initial_value_wrtten = False

    def __call__(self, event: Event):
        serialized = event.json()
        if self.initial_value_wrtten:
            self.writer.write(",\n")
        self.writer.write(serialized)
        self.writer.flush()
        self.initial_value_wrtten = True

    def __exit__(self, **kwargs):
        if self.initial_value_wrtten:
            self.writer.write("\n")
        self.writer.write("]\n")
        self.writer.flush()
        self.writer.__exit__(**kwargs)