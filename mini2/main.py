from multiprocessing import Process
import time
import requests
import signal
import sys

from src.utilities.colors import print_red, print_yellow
from src.ring.rest.server import start_rest_server_by_mode
from src.ring.rest.central_hub import start_rest_hub_by_mode
from src.ring.rest.client import test_rest_client, run_rest_discovery
from src.ring.grpc.client import test_grpc_client, run_grpc_discovery
from src.ring.grpc.server import start_grpc_server_by_mode
from src.ring.grpc.central_hub import start_grpc_hub_by_mode
from src.utilities.modes import ServerMode, ServerURLS

from src.star.rest.central_hub import (
    start_rest_hub_by_mode as start_rest_hub_by_mode_star,
)
from src.star.rest.server import (
    start_rest_server_by_mode as start_rest_server_by_mode_star,
)
from src.star.rest.client import test_rest_client as test_rest_client_star
from src.star.grpc.central_hub import (
    start_grpc_hub_by_mode as start_grpc_hub_by_mode_star,
)
from src.star.grpc.server import (
    start_grpc_server_by_mode as start_grpc_server_by_mode_star,
)
from src.star.grpc.client import test_grpc_client as test_grpc_client_star

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


class STAR:
    def __init__(self):
        pass

    @classmethod
    def run_tests(self):
        print("--------------------------REST--------------------------")
        rest = self.run_rest()
        print("\n\n")
        print("--------------------------GRPC--------------------------")
        grpc = self.run_grpc()
        print("Rest: ", rest, "GRPC: ", grpc)
        cleanup()

    @classmethod
    def run_rest(self):
        global processes
        result = None

        # Register signal handler for graceful termination
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start the servers
        processes = [
            Process(target=start_rest_server_by_mode_star, args=(ServerMode.SERVER1,)),
            Process(target=start_rest_server_by_mode_star, args=(ServerMode.SERVER2,)),
            Process(target=start_rest_server_by_mode_star, args=(ServerMode.SERVER3,)),
            Process(
                target=start_rest_hub_by_mode_star,
                args=(ServerURLS.SERVER1, ServerURLS.SERVER2, ServerURLS.SERVER3),
            ),
        ]

        for process in processes:
            process.start()

        time.sleep(2)

        print_yellow("Testing client using RestAPI...")
        result = test_rest_client_star(ServerURLS.HUB, ServerURLS.SERVER2)

        cleanup()
        return result

    @classmethod
    def run_grpc(self):
        global processes
        result = None

        # Register signal handler for graceful termination
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start the servers
        processes = [
            Process(target=start_grpc_server_by_mode_star, args=(ServerMode.SERVER1,)),
            Process(target=start_grpc_server_by_mode_star, args=(ServerMode.SERVER2,)),
            Process(target=start_grpc_server_by_mode_star, args=(ServerMode.SERVER3,)),
            Process(
                target=start_grpc_hub_by_mode_star,
                args=(ServerURLS.SERVER1, ServerURLS.SERVER2, ServerURLS.SERVER3),
            ),
        ]

        for process in processes:
            process.start()

        time.sleep(2)

        print_yellow("Testing client using GRPC...")
        result = test_grpc_client_star(ServerURLS.HUB, ServerURLS.SERVER2)

        cleanup()
        return result


class RING:
    def __init__(self):
        pass

    @classmethod
    def run_tests(self):
        print("--------------------------REST--------------------------")
        rest = self.run_rest()
        print("\n\n")
        print("--------------------------GRPC--------------------------")
        grpc = self.run_grpc()
        print("Rest: ", rest, "GRPC: ", grpc)
        cleanup()

    @classmethod
    def run_rest(self):
        global processes
        result = None

        # Register signal handler for graceful termination
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start the servers
        processes = [
            Process(target=start_rest_server_by_mode, args=(ServerMode.SERVER1,)),
            Process(target=start_rest_server_by_mode, args=(ServerMode.SERVER2,)),
            Process(target=start_rest_server_by_mode, args=(ServerMode.SERVER3,)),
            Process(target=start_rest_hub_by_mode),
        ]

        for process in processes:
            process.start()

        time.sleep(2)

        print("\n\nDiscovering servers...\n")
        response = run_rest_discovery(ServerURLS.HUB)

        if response.status_code == 200:
            print_yellow("Testing client using RestAPI...")
            result = test_rest_client(ServerURLS.HUB, ServerURLS.SERVER2)

        cleanup()
        return result

    @classmethod
    def run_grpc(self):
        global processes
        result = None

        # Register signal handler for graceful termination
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start the servers
        processes = [
            Process(target=start_grpc_server_by_mode, args=(ServerMode.SERVER1,)),
            Process(target=start_grpc_server_by_mode, args=(ServerMode.SERVER2,)),
            Process(target=start_grpc_server_by_mode, args=(ServerMode.SERVER3,)),
            Process(target=start_grpc_hub_by_mode),
        ]

        for process in processes:
            process.start()

        time.sleep(2)

        print("\n\nDiscovering servers...\n")
        response = run_grpc_discovery(ServerURLS.HUB)

        if response.success:
            print_yellow("Testing client using GRPC...")
            result = test_grpc_client(ServerURLS.HUB, ServerURLS.SERVER2)

        cleanup()
        return result


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print_red("Usage: python main.py <TOPOLOGY>")
        sys.exit(1)

    TOPOLOGY = sys.argv[1]
    try:
        if TOPOLOGY == "RING":
            RING.run_tests()
        elif TOPOLOGY == "STAR":
            STAR.run_tests()

    except Exception as e:
        print(f"An error occurred: {e}")
        cleanup_and_exit()

    except KeyboardInterrupt:
        cleanup_and_exit()
