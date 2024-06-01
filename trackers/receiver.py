from contextlib import contextmanager, AbstractContextManager

TReceiver = AbstractContextManager

@contextmanager
def configure_receiver(receiver: TReceiver):
    with receiver:
        yield
    
