from json import loads
import pickle
from trackers.json import Event, Phase

def test_simple_json():
    e = Event("name", "cat", 0, 0, Phase.B, 123, {"a":"b"})
    assert e.json() == r'{"name":"name","cat":"cat","ph":"B","ts":123,"ts":123,"pid":0,"tid":0,"args":{"a": "b"}}'
    assert loads(e.json())["name"] == "name"

def test_simple_mandatory_json():
    e = Event(None, None, 0, 0, Phase.E, 123, None)
    assert e.json() == r'{"ph":"E","ts":123,"ts":123,"pid":0,"tid":0}'
    assert loads(e.json())["ts"] == 123

def test_event_pkl():
    e = Event("name", "cat", 0, 0, Phase.B, 123, {"a":"b"})
    serialized = pickle.loads(pickle.dumps(e))
    assert serialized.cat == "cat"