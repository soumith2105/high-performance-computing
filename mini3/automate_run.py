from multiprocessing import Process
from random import randint
import threading
import time
import requests
import signal
import sys

from src.utilities.colors import print_red, print_cyan
from src.server import start_rest_server_by_mode
from src.client import test_rest_client, run_rest_discovery
from src.utilities.modes import ModeConfiguration

processes = []  # To keep track of all spawned processes


def cleanup():
    """Terminate all processes."""
    print("\nTerminating all services...")
    for process in processes:
        if process.is_alive():
            process.terminate()

    processes.clear()


def cleanup_and_exit():
    cleanup()
    sys.exit(1)


def signal_handler(signum, frame):
    """Handle termination signals (e.g., Ctrl+C)."""
    cleanup_and_exit()

class RING:
    def __init__(self):
        pass

    @classmethod
    def run_tests(self, server_count):
        print("--------------------------REST--------------------------")
        self.run_rest(server_count)
        cleanup()

    @classmethod
    def run_rest(self, server_count):
        global processes
        result = None
        self.server_urls = []

        # Register signal handler for graceful termination
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start the servers
        for i in range(server_count):
            self_url =  f'127.0.0.1:800{i}'
            self.server_urls.append(self_url)
            left_url = f'127.0.0.1:800{(i-1)%server_count if i-1 >= 0 else server_count+(i-1)}'
            right_url = f'127.0.0.1:800{(i+1)%server_count}'
            print(self_url, left_url, right_url)
            processes.append(Process(target=start_rest_server_by_mode, args=(ModeConfiguration(f'SERVER-{i+1}', self_url=self_url, left_url=left_url, right_url=right_url), i)))


        for process in processes:
            process.start()

        time.sleep(5)
        
        def drop_servers():
            while len(self.server_urls) > 3:
                time.sleep(randint(15, 20))
                id = randint(0, len(self.server_urls)-1)
                url = self.server_urls.pop(id)
                print_cyan(f"Dropping a server {url}")
                processes[id].terminate()
                processes.pop(id)
        
        threading.Thread(target=drop_servers, daemon=True).start()
        
        while True:
            test_rest_client(self.server_urls[randint(0,len(self.server_urls)-1)])
            time.sleep(randint(4, 8))
        
        
        cleanup()
        return result


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print_red("Usage: python main.py <TOPOLOGY>")
        sys.exit(1)

    SERVER_COUNT = int(sys.argv[1])
    try:
        RING.run_tests(SERVER_COUNT)

    except Exception as e:
        print(f"An error occurred: {e}")
        cleanup_and_exit()

    except KeyboardInterrupt:
        cleanup_and_exit()
