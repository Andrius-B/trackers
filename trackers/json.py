from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional, Union
from json import dumps


TJSON_VALUE = Optional[Union[str, float, bool]]
Phase = Enum('Phase', ["B", "E", "C"])


@dataclass
class Event:
    name: Optional[str]
    cat: Optional[str]
    pid: int
    tid: int
    ph: Phase
    ts: int
    args: Optional[Mapping[str, TJSON_VALUE]]

    def json(self):
        # based on https://docs.google.com/document/d/1CvAClvFfyA5R-PhYUmn5OOQtYMH4h6I0nSsKchNAySU/preview#heading=h.nso4gcezn7n1
        # render a string like like: {"name": "myFunction", "cat": "foo", "ph": "B", "ts": 123, "pid": 2343, "tid": 2347,"args": {"first": 1}},
        name_str = "" if self.name is None else f"\"name\":\"{self.name}\","
        cat_str = "" if self.cat is None else f"\"cat\":\"{self.cat}\","
        args_str = "" if self.cat is None else f",\"args\":{dumps(self.args)}"
        return f"{{{name_str}{cat_str}\"ph\":\"{self.ph.name}\",\"ts\":{self.ts},\"ts\":{self.ts},\"pid\":{self.pid},\"tid\":{self.tid}{args_str}}}"