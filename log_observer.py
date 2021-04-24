from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import re
import multiprocessing
from check_log_list import check_log_in_sequence
import logging

mylogger = logging.getLogger(__name__)
mylogger.setLevel(level=logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(message)s")
streamHandler.setFormatter(formatter)
mylogger.addHandler(streamHandler)


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
                 case_sensitive=True, ignore_directories=True, clearlog=True):
        self.event_handler = EventHandler(patterns=pattern, ignore_patterns=ignore_pattern,
                            ignore_directories=ignore_directories, case_sensitive=case_sensitive,
                                filename=filename, logpattern=logpattern, clearlog=clearlog)
        self.path = path
        self.recursive = recursive
        self.observer = Observer()

    def __enter__(self):
        self.observer.schedule(self.event_handler, self.path, recursive=self.recursive)
        self.observer.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.observer.stop()
        self.observer.join()


def run_obersver(pattern, ignore_pattern, filename, log_pattern, path, events):
    counter = 0
    with LogObserver(pattern, ignore_pattern, filename, log_pattern, path) as obs:
        while 1:
            counter += 1
            result = check_log_in_sequence(events, log_list)
            time.sleep(1)
            if result:
                break
    mylogger.info(f"Breaking run_observer")


def save_log():
    print("Generating attach logs")
    for i in range(300):
        with open("logging.log", "a") as f:
            f.writelines(str(i))
        time.sleep(0.01)


def wait_until_observer_completed(observer, tmout):
    counter = 0
    mylogger.info(f"Observing for {tmout} seconds")
    try:
        while 1:
            mylogger.info(f"Observer status {observer.is_alive()}")
            if not observer.is_alive():
                mylogger.info(f"Observer completed successfully")
                return True
            else:
                time.sleep(1)
                counter += 1
                mylogger.info(f"Continue observation, remaining {tmout - counter} seconds")
                if counter == tmout:
                    observer.terminate()
                    time.sleep(1)
                    mylogger.info(f"Observed provess killed, observer status is_alive = {observer.is_alive()}")
                    raise TimeoutError
    except TimeoutError:
        mylogger.info(f"Timeout Error")


def start_observer_process(pattern, ignore_pattern, filename, log_pattern, path, events):
    mylogger.info(f"Starting observer process, observing for events: {events} ")
    obs_process = multiprocessing.Process(target=run_obersver, args=[pattern, ignore_pattern, filename, log_pattern, path, events])
    obs_process.start()
    return obs_process


def attach_ue():
    print("Attaching UE")

path = "."
filename = "logging.log"
pattern = "*"
ignore_pattern = ""
log_pattern = r".*"

generating_logs_process = multiprocessing.Process(target=save_log)

if __name__ == "__main__":
    obs = start_observer_process(path=path, filename=filename, pattern=pattern, ignore_pattern=ignore_pattern,
                                 log_pattern=log_pattern, events=['9', '100', '11', '12'])
    time.sleep(1)
    attach_ue()
    generating_logs_process.start()
    wait_until_observer_completed(obs, 30)







