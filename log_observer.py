from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import re
import multiprocessing
from check_log_list import check_log_in_sequence



log_list = list()
event = ["200", "201", "202", "203"]


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


def run_obersver(pattern, ignore_pattern, filename, log_pattern, path, tmout=10):
    counter = 0
    with LogObserver(pattern, ignore_pattern, filename, log_pattern, path) as obs:
        try:
            while 1:
                counter += 1
                result = check_log_in_sequence(event, log_list)
                if result:
                    print(f"Observer completed successfully, {event} found in {log_list}")
                    return 1
                if counter == tmout:
                    raise TimeoutError
                time.sleep(1)
        except TimeoutError as t:
            print("Timeout Error")


def save_log():
    print("Generating attach logs")
    for i in range(300):
        with open("logging.log", "a") as f:
            f.writelines(str(i))
        time.sleep(0.1)


path = "."
filename = "logging.log"
pattern = "*"
ignore_pattern = ""
log_pattern = r".*"

p1 = multiprocessing.Process(target=run_obersver, args=[pattern, ignore_pattern, filename, log_pattern, path, 600])


def start_process(process):
    process.start()


def is_process_alive(process):
    return process.is_alive()


def attach_ue():
    print("Attaching UE")


if __name__ == "__main__":
    start_process(p1)
    time.sleep(1)
    attach_ue()
    save_log()




