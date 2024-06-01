import socket
from trackers.json import Event


class TCPDispatcher:
    def __init__(self, port: int = 61432) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(("localhost", port))

    def __call__(self, event: Event):
        self._socket.sendall(f"{event.json()}\n".encode())

    def __exit__(self, **_):
        self._socket.close()
