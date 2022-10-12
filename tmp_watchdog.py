import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.event_type == "modified":
            print("event handler")


if __name__ == "__main__":
    w = Watcher(
        "/Users/thom/code/resolve-ui/src/log/proxy_runner.log", MyHandler()
    )
    w.run()
