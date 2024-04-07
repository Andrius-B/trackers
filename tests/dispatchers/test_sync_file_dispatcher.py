from json import loads
from tests.test_fixtures import temp_file_closed
from trackers.dispatchers.sync_file_dispatcher import SyncFileDispatcher
from trackers.dispatcher import configure_dispatcher
from trackers.trackers import track

def test_sync_file_dispatcher():
    with temp_file_closed() as f:
        with configure_dispatcher(SyncFileDispatcher(f)):
            with track("n", "c"):
                pass
        lines = f.read_text().splitlines()
        assert len(lines) == 4
        assert loads(f.read_text()), "Profile json file loadable"

 