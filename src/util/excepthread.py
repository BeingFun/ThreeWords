import threading
import traceback


class ExcThread(threading.Thread):
    def __init__(self, target=None, *args, name=None, **kwargs):
        if name is None:
            name = target.__name__
        super(ExcThread, self).__init__(None, target, name, args, kwargs)
        self.exit_code = None
        self.exception = None
        self.exc_traceback = None
        self.daemon = True
        self.name = name
        self.target = target

    def run(self):
        try:
            self._run()
        except Exception as e:
            self.exception = e
            self.exit_code = 1
            self.exc_traceback = traceback.format_exc()
        except SystemExit as e:
            self.exit_code = e.code

    def _run(self):
        try:
            self._target(*self._args, **self._kwargs)
        except Exception as e:
            raise e
