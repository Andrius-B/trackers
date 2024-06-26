from threading import Thread
from contextlib import contextmanager
from trackers.redispatchers.tcp_redispatcher import TCPMetricsSocketHandler
from trackers.dispatchers.tcp_dispatcher import TCPDispatcher
from trackers.dispatcher import configure_dispatcher
from trackers.json import Event
from trackers.trackers import tracked
import socketserver
from multiprocessing import Process


class TCPMetricsTestHandler(TCPMetricsSocketHandler):
    events: list[Event] = []

    def handle_event(self, event: Event):
        TCPMetricsTestHandler.events.append(event)


def _run_test_tcp_server(port: int, host: str):
    with socketserver.TCPServer((host, port), TCPMetricsTestHandler) as server:
        server.timeout = 0.05
        while not TCPMetricsTestHandler.termination_event.is_set():
            server.handle_request()


TEST_PORT_1 = 12154


@contextmanager
def tcp_test_receiver_thread(port: int, host: str = "localhost"):
    TCPMetricsTestHandler.events = []
    TCPMetricsTestHandler.termination_event.clear()
    server_thread = Thread(
        target=_run_test_tcp_server,
        args=(port, host),
        name="test-tcp-metric-listener",
        daemon=True,
    )
    server_thread.start()
    assert server_thread.is_alive(), "Thread not started yet!"
    TCPMetricsTestHandler.started = True
    yield server_thread
    TCPMetricsTestHandler.termination_event.set()
    server_thread.join(timeout=1)
    TCPMetricsTestHandler.started = False
    assert (
        not server_thread.is_alive()
    ), "TCPMetricsHandler server did not terminate in time."


def test_tcp_dispatcher_metrics_from_main_thread():
    with tcp_test_receiver_thread(TEST_PORT_1):
        with configure_dispatcher(TCPDispatcher(TEST_PORT_1)):
            for i in range(100):
                with tracked(f"{i}", "c"):
                    pass
            for i in range(100):
                with tracked(f"2-{i}", "c"):
                    pass
    # two ranges sending 100 start and end events = 400 events
    assert len(TCPMetricsTestHandler.events) == 400


TEST_PORT_2 = TEST_PORT_1 + 1


def send_from_process1():
    with configure_dispatcher(TCPDispatcher(TEST_PORT_2)):
        for i in range(50):
            with tracked(f"first-{i}", "c"):
                pass


def send_from_process2():
    with configure_dispatcher(TCPDispatcher(TEST_PORT_2)):
        for i in range(50):
            with tracked(f"second-{i}", "c"):
                pass


def test_tcp_dispatcher_metrics_from_process():
    with tcp_test_receiver_thread(port=TEST_PORT_2):
        procs = [Process(target=f) for f in [send_from_process1, send_from_process2]]
        TCPMetricsTestHandler.events = []
        for p in procs:
            p.start()
        for p in procs:
            p.join()
    # two processes sending 50 start and end events = 200 events
    assert len(TCPMetricsTestHandler.events) == 200
