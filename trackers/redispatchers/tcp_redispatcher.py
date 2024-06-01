from types import TracebackType
from typing import Any
import socketserver
from threading import Event, Thread
from contextlib import contextmanager
from json import loads
from trackers.dispatcher import TDispatcher
from trackers.redispatcher import Redispatcher


class TCPMetricsSocketHandler(socketserver.BaseRequestHandler):
    started = False
    base_dispatcher: TDispatcher = None
    termination_event = Event()

    def handle(self):
        for sample_bytes in self.read_request_lines():
            self.handle_one_sample(sample_bytes)

    def handle_one_sample(self, sample_bytes: bytes):
        self.handle_event(loads(sample_bytes.decode()))

    def handle_event(self, event: Event):
        TCPMetricsSocketHandler.base_dispatcher(event)

    def read_request_chunk(self, chunk_size=1024):
        while len(data := self.request.recv(chunk_size)) > 0:
            yield data
        yield data

    def read_request_lines(self):
        buffer: bytes = b""
        for chunk in self.read_request_chunk():
            buffer += chunk
            while b"\n" in buffer:
                first_newline = buffer.find(b"\n")
                sample, buffer = buffer[:first_newline], buffer[first_newline + 1 :]
                yield sample


def _run_tcp_server(port: int, host: str):
    with socketserver.TCPServer((host, port), TCPMetricsSocketHandler) as server:
        server.timeout = 0.05
        while not TCPMetricsSocketHandler.termination_event.is_set():
            server.handle_request()


@contextmanager
def _tcp_redispatcher_thread(
    base_dispathcer: TDispatcher, port: int = 12153, host: str = "localhost"
):
    TCPMetricsSocketHandler.base_dispatcher = base_dispathcer
    TCPMetricsSocketHandler.termination_event.clear()
    server_thread = Thread(
        target=_run_tcp_server,
        args=(port, host),
        name="tcp-metric-listener",
        daemon=True,
    )
    server_thread.start()
    TCPMetricsSocketHandler.started = True
    yield server_thread
    TCPMetricsSocketHandler.termination_event.set()
    server_thread.join(timeout=0.1)
    TCPMetricsSocketHandler.started = False
    TCPMetricsSocketHandler.base_dispatcher = None
    assert (
        not server_thread.is_alive()
    ), "TCPMetricsHandler server did not terminate in time."


class TCPRedispatcher(Redispatcher):
    def __init__(
        self, dispatcher: TDispatcher, port: int = 12153, host: str = "localhost"
    ) -> None:
        super().__init__(dispatcher)
        self.redispatcher_thread_context_manager = _tcp_redispatcher_thread(
            base_dispathcer=dispatcher, port=port, host=host
        )

    def __enter__(self) -> Any:
        super().__enter__()
        self.redispatcher_thread_context_manager.__enter__()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        super().__exit__(exc_type, exc_value, traceback)
        self.redispatcher_thread_context_manager.__exit__(
            exc_type, exc_value, traceback
        )
