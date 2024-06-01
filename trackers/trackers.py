from typing import Optional, Mapping
from contextlib import contextmanager
from threading import get_ident
from os import getpid
from time import perf_counter_ns
from trackers.json import Event, Phase
import trackers.dispatcher as d


@contextmanager
def tracked(name: str, cat: str, args: Optional[Mapping] = None):
    common_args = {
        "name": name,
        "cat": cat,
        "pid": getpid(),
        "tid": get_ident(),
    }
    # divide to deliver microseconds in the event
    d._dispatcher(Event(**common_args, args=args, ph=Phase.B, ts=perf_counter_ns() // 1000))
    yield
    d._dispatcher(Event(**common_args, args=None, ph=Phase.E, ts=perf_counter_ns() // 1000))
