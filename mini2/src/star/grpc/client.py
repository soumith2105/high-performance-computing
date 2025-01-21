import grpc
import src.star.grpc.star_service_pb2 as star_service_pb2
import src.star.grpc.star_service_pb2_grpc as star_service_pb2_grpc
import time


def client_send_message(central_hub_url, target, message):
    """
    Sends a message to the central hub and measures the time taken.
    """
    start_time = time.time()

    with grpc.insecure_channel(
        central_hub_url,
        options=[("grpc.max_receive_message_length", 1024 * 1024 * 1024)],
    ) as channel:
        stub = star_service_pb2_grpc.DataProcessorStub(channel)
        response = stub.GetObjectOfArray(  # Change this to GetArrayOfObject to test the other method
            star_service_pb2.DataRequest(message=message, target=target)
        )

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Time taken: {elapsed_time:.4f} seconds")
    return elapsed_time


def test_grpc_client(hub_url, target_url):
    message = "Hello, Server 2!"
    return client_send_message(hub_url, target_url, message)
