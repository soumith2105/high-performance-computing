import requests
import time

from src.utilities.modes import ServerURLS


def client_send_message(central_hub_url, target, message):
    payload = {"target": target, "message": message}
    start_time = time.time()

    response = requests.post(f"http://{central_hub_url}/send_message", json=payload)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.4f} seconds")
    return elapsed_time


def test_rest_client(hub_url, target_url):
    message = "Hello, Server 2!"
    return client_send_message(hub_url, target_url, message)


def run_rest_discovery(hub_url):
    response = requests.get(f"http://{hub_url}/discover")
    return response
