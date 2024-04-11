from json import loads
import time
from threading import Thread
from tests.test_fixtures import temp_file_closed
from trackers.dispatchers.tcp_dispatcher import TCPDispatcher
from trackers.dispatcher import configure_dispatcher
from trackers.trackers import track
import socketserver
from multiprocessing import Process

class TCPMetricsHandler(socketserver.BaseRequestHandler):

    samples = []

    def handle_one_sample(self, sample_bytes: bytes):
        try:
            TCPMetricsHandler.samples.append(loads(sample_bytes.decode()))
        except Exception as e:
            raise e
    def read_request_lines(self):
        buffer = b''
        while len(data := self.request.recv(1024)) > 0:
            buffer += data
            while b'\n' in buffer:
                first_newline = buffer.find(b'\n')
                sample, buffer = buffer[:first_newline], buffer[first_newline+1:]
                yield sample
            print(f"Received sent {len(TCPMetricsHandler.samples)} events")

    def handle(self):
        for sample_bytes in self.read_request_lines():
            self.handle_one_sample(sample_bytes)
        

PORT = 12153

def run_tcp_server():
    with socketserver.TCPServer(("localhost", PORT), TCPMetricsHandler) as server:
        server.handle_request()

def test_tcp_dispatcher_metrics_from_main_thread():
    server_thread = Thread(target = run_tcp_server, name = "tcp-metric-listener", daemon=True)
    server_thread.start()
    TCPMetricsHandler.samples = []
    with configure_dispatcher(TCPDispatcher(PORT)):
        for i in range(100):
            with track(f"{i}", "c"):
                pass
        for i in range(100):
            with track(f"2-{i}", "c"):
                pass
    server_thread.join(timeout=0.1)
    assert len(TCPMetricsHandler.samples) == 400


def send_from_process1():
    with configure_dispatcher(TCPDispatcher(PORT)):
        for i in range(50):
            with track(f"first-{i}", "c"):
                pass
def send_from_process2():
    with configure_dispatcher(TCPDispatcher(PORT)):
        for i in range(50):
            with track(f"second-{i}", "c"):
                pass

def test_tcp_dispatcher_metrics_from_process():
    server_thread = Thread(target = run_tcp_server, name = "tcp-metric-listener", daemon=True)
    server_thread.start()
    procs = [Process(target=f) for f in [send_from_process1, send_from_process2]]
    TCPMetricsHandler.samples = []
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    # 2 processes sending start and end events 50 times means 200 events in total
    assert len(TCPMetricsHandler.samples) == 200
    server_thread.join(timeout=0.1)


 