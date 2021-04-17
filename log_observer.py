from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import re
log_list = list()


class EventHandler(PatternMatchingEventHandler):

    def __init__(self, patterns, ignore_patterns, ignore_directories,
                 case_sensitive, filename, logpattern=None, clearlog=False):
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)
        self.filename = filename
        self.logpattern = re.compile(logpattern, re.M) if logpattern is not None else None
        if clearlog:
            with open(self.filename, "w") as f:
                f.flush()
                self.position = 0
        else:
            with open(self.filename, "r") as f:
                f.read()
                self.position = f.tell()

    def on_modified(self, event):
        with open(self.filename, "r") as f:
            f.seek(self.position)
            line = f.readline()
            self.position = f.tell()
            if self.logpattern.search(line):
                log_list.append(line.strip()) if line not in ["", "\n"] else None


class LogObserver:

    def __init__(self, pattern, ignore_pattern,
                filename, logpattern, path, recursive=False,
                 case_sensitive=True, ignore_directories=True):
        self.event_handler = EventHandler(patterns=pattern, ignore_patterns=ignore_pattern,
                            ignore_directories=ignore_directories, case_sensitive=case_sensitive,
                                filename=filename, logpattern=logpattern, clearlog=True)
        self.path = path
        self.recursive = recursive
        self.observer = Observer()

    def __enter__(self):
        self.observer.schedule(self.event_handler, self.path, recursive=self.recursive)
        self.observer.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.observer.stop()
        self.observer.join()



path = "../../udemy"
filename = "../../udemy/logging.log"
pattern = "*"
ignore_pattern = ""
log_pattern = r"^[1-9]*$"

with LogObserver(pattern, ignore_pattern, filename, log_pattern, path) as obs:
    try:
        while 1:
            print(log_list)
            if "123" in log_list:
                raise KeyboardInterrupt
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Log found")







