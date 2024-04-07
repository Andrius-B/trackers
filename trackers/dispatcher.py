from typing import Callable
from trackers.json import Event
from contextlib import contextmanager

def unconfigured_dispatcher(e: Event) -> None:
    raise NotImplementedError("The dispatcher is not configured correctly")

TDispatcher = Callable[[Event], None]

# this is intentionally a singleton-like global configuration
_dispatcher: TDispatcher = unconfigured_dispatcher

@contextmanager
def configure_dispatcher(temporary_dispatcher: TDispatcher):
    global _dispatcher
    prev_dispatcher = _dispatcher
    _dispatcher = temporary_dispatcher
    yield
    _dispatcher = prev_dispatcher
    exit_func = getattr(temporary_dispatcher, "__exit__", None)
    if callable(exit_func):
        exit_func()



def set_default_dispatcher(default_dispatcher: TDispatcher):
    global _dispatcher
    _dispatcher = default_dispatcher

def reset_default_dispatcher():
    global _dispatcher
    exit_func = getattr(_dispatcher, "__exit__", None)
    _dispatcher = unconfigured_dispatcher
    if callable(exit_func):
        exit_func()
    
