import grpc
import time

import src.ring.grpc.ring_pb2 as ring_pb2
import src.ring.grpc.ring_pb2_grpc as ring_pb2_grpc
from src.utilities.modes import ServerURLS


def client_send_message(central_hub_url, target, message):
    """
    Sends a message to the central hub and measures the time taken.
    """
    start_time = time.time()

    with grpc.insecure_channel(
        central_hub_url,
        options=[("grpc.max_receive_message_length", 1024 * 1024 * 1024)],
    ) as channel:
        stub = ring_pb2_grpc.CentralHubStub(channel)
        response = stub.GetObjectOfArray(  # Change this to GetArrayOfObject to test the other method
            ring_pb2.RelayMessage(target=target, message=message)
        )

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Time taken: {elapsed_time:.4f} seconds")
    return elapsed_time


def test_grpc_client(hub_url, target_url):
    message = "Hello, Server 2!"
    return client_send_message(hub_url, target_url, message)


def run_grpc_discovery(hub_url):
    with grpc.insecure_channel(hub_url) as channel:
        stub = ring_pb2_grpc.CentralHubStub(channel)
        response = stub.Discover(ring_pb2.DiscoverRequest())
        return response
