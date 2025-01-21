import requests
import time


def client_send_message(central_hub_url, target, message):
    payload = {"target": target, "message": message}
    start_time = time.time()

    response = requests.post(f"http://{central_hub_url}/process", json=payload)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.4f} seconds")
    return elapsed_time


def test_rest_client(hub_url, target_url):
    message = "Hello, Server 2!"
    return client_send_message(hub_url, target_url, message)
