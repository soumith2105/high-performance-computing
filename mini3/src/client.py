import requests
import time
from random import randint
from typing import List
from src.utilities.colors import print_blue

UUID = 1


def client_send_message(server_url: str, task_count: int) -> None:
    global UUID
    payload = []
    for i in range(task_count):
        payload.append({"task": f"Task {UUID}", "timeout": randint(4, 6)})
        UUID += 1

    url = f"http://{server_url}/add_task"
    print_blue(f"Sending {len(payload)} task to {url}")
    requests.post(url, json=payload)


def test_rest_client(server_url):
    client_send_message(server_url=server_url, task_count=randint(1, 10))


def run_rest_discovery(hub_url):
    response = requests.get(f"http://{hub_url}/discover")
    return response
