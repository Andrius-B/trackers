import socketserver
from threading import Event, Thread
from contextlib import contextmanager
from json import loads

class TCPMetricsSocketHandler(socketserver.BaseRequestHandler):
    started = False
    events: list[Event] = []
    termination_event = Event()

    def handle(self):
        for sample_bytes in self.read_request_lines():
            self.handle_one_sample(sample_bytes)

    def handle_one_sample(self, sample_bytes: bytes):
        try:
            self.handle_event(loads(sample_bytes.decode()))
        except Exception as e:
            raise e
        
    def handle_event(self, event: Event):
        TCPMetricsSocketHandler.events.append(event)
        
    def read_request_chunk(self, chunk_size = 1024):
        while len(data := self.request.recv(chunk_size)) > 0:
            yield data
        yield data

    def read_request_lines(self):
        buffer: bytes = b''
        for chunk in self.read_request_chunk():
            buffer += chunk
            while b'\n' in buffer:
                first_newline = buffer.find(b'\n')
                sample, buffer = buffer[:first_newline], buffer[first_newline+1:]
                yield sample

def _run_tcp_server(port: int, host: str):
    with socketserver.TCPServer((host, port), TCPMetricsSocketHandler) as server:
        server.timeout = 0.05
        while not TCPMetricsSocketHandler.termination_event.is_set():
            server.handle_request()

@contextmanager
def tcp_redispatcher_thread(port: int = 12153, host: str = "localhost"):
    TCPMetricsSocketHandler.events = []
    TCPMetricsSocketHandler.termination_event.clear()
    server_thread = Thread(target = _run_tcp_server, args = (port, host), name = "tcp-metric-listener", daemon=True)
    server_thread.start()
    TCPMetricsSocketHandler.started = True
    yield server_thread
    TCPMetricsSocketHandler.termination_event.set()
    server_thread.join(timeout=0.1)
    TCPMetricsSocketHandler.started = False
    assert not server_thread.is_alive(), "TCPMetricsHandler server did not terminate in time."