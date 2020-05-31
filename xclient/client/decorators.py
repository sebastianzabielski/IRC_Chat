import threading
from xclient.client.utils import Sender


def request_action():
    def inner(f):
        def func(*args, **kwargs):
            send_thread = threading.Thread(target=Sender.send_message(f, *args, **kwargs))
            send_thread.start()

        return func

    return inner
