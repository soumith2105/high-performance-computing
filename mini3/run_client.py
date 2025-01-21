from multiprocessing import Process
from random import randint
import threading
import time
import requests
import signal
import sys

from src.utilities.colors import print_red
from src.server import start_rest_server_by_mode
from src.client import client_send_message
from src.utilities.modes import ModeConfiguration


def cleanup_and_exit():
    sys.exit(1)


def signal_handler(signum, frame):
    """Handle termination signals (e.g., Ctrl+C)."""
    cleanup_and_exit()


def run_rest(server_url, left_url, right_url):
    # Register signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    def get_url(server_port):
        return f"127.0.0.1:{server_port}"

    print("Starting REST server... in 10 seconds")
    time.sleep(10)

    start_rest_server_by_mode(
        ModeConfiguration(
            server_url,
            self_url=get_url(server_url),
            left_url=get_url(left_url),
            right_url=get_url(right_url),
        ),
        0,
    )


if __name__ == "__main__":
    try:
        while True:
            server_url = input("Enter server url: ")
            task_count = int(input("Enter task count: "))
            client_send_message(f"127.0.0.1:{server_url}", task_count)

    except Exception as e:
        print(f"An error occurred: {e}")
        cleanup_and_exit()

    except KeyboardInterrupt:
        cleanup_and_exit()
