from typing import Optional, MutableMapping, Mapping
from contextlib import contextmanager
from threading import get_ident
from os import getpid
from time import perf_counter_ns
from trackers.json import Event, Phase, TJSON_VALUE
import trackers.dispatcher as d

def _make_common_args(name: str, cat: str):
    return {
        "name": name,
        "cat": cat,
        "pid": getpid(),
        "tid": get_ident(),
    }

@contextmanager
def tracked(name: str, cat: str, args: Optional[Mapping[str, TJSON_VALUE]] = None):
    common_args = _make_common_args(name, cat)
    # divide to deliver microseconds in the event
    d._dispatcher(Event(**common_args, args=args, ph=Phase.B, ts=perf_counter_ns() // 1000))
    yield
    d._dispatcher(Event(**common_args, args=None, ph=Phase.E, ts=perf_counter_ns() // 1000))

def gauge(name: str, cat: str, value: float, args: Optional[MutableMapping[str, TJSON_VALUE]] = None):
    common_args = _make_common_args(name, cat)
    args_dict: MutableMapping[str, TJSON_VALUE] = args or {}
    args_dict["value"] = value
    d._dispatcher(Event(**common_args, args=args_dict, ph=Phase.C, ts=perf_counter_ns() // 1000))
