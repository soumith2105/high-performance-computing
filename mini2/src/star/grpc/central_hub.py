import grpc
from concurrent import futures
from src.utilities.colors import print_blue
from src.utilities.modes import (
    ModeConfiguration,
    ServerMode,
    ServerURLS,
    get_configuration,
)
from src.utilities.print_prefix import set_print_prefix
import src.star.grpc.star_service_pb2 as star_service_pb2
import src.star.grpc.star_service_pb2_grpc as star_service_pb2_grpc
from typing import List


class DataProcessor(star_service_pb2_grpc.DataProcessorServicer):
    def __init__(self, modeConfig: ModeConfiguration, SLAVE_SERVERS: List[str]):
        self.HOST = modeConfig.self_url
        self.SERVER_NAME = modeConfig.server_name
        self.SLAVE_SERVERS = SLAVE_SERVERS

        # Set server configurations
        set_print_prefix(self.SERVER_NAME)

    def ProcessData(self, request, context):
        target = request.target

        if target not in self.SLAVE_SERVERS:
            return star_service_pb2.DataResponse(
                reply=f"Error: Target slave '{target}' is not valid.",
            )

        print_blue(f"Routing message '{request.message}' to {target}")
        with grpc.insecure_channel(target) as channel:
            stub = star_service_pb2_grpc.DataProcessorStub(channel)
            response = stub.ProcessData(
                star_service_pb2.DataRequest(message=request.message)
            )

            return star_service_pb2.DataResponse(reply=response.reply)

    def GetArrayOfObject(self, request, context):
        target = request.target
        print_blue(f"Routing message '{request.message}' to {target}")
        # Forward the message to the next server
        with grpc.insecure_channel(
            target,
            options=[("grpc.max_receive_message_length", 1024 * 1024 * 1024)],
        ) as channel:
            stub = star_service_pb2_grpc.DataProcessorStub(channel)
            response = stub.GetArrayOfObject(request)
            return response

    def GetObjectOfArray(self, request, context):
        target = request.target
        print_blue(f"Routing message '{request.message}' to {target}")
        # Forward the message to the next server
        with grpc.insecure_channel(
            target,
            options=[("grpc.max_receive_message_length", 1024 * 1024 * 1024)],
        ) as channel:
            stub = star_service_pb2_grpc.DataProcessorStub(channel)
            response = stub.GetObjectOfArray(request)
            return response


def start_grpc_hub(modeConfig: ModeConfiguration, SLAVE_SERVERS: List[str]):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_send_message_length", 1024 * 1024 * 1024),  # 10 MB
            ("grpc.max_receive_message_length", 1024 * 1024 * 1024),  # 10 MB
        ],
    )
    star_service_pb2_grpc.add_DataProcessorServicer_to_server(
        DataProcessor(modeConfig, SLAVE_SERVERS), server
    )
    server.add_insecure_port(ServerURLS.HUB)
    server.start()
    print("Central hub server running...")
    server.wait_for_termination()


def start_grpc_hub_by_mode(*SLAVE_SERVERS: List[str]) -> None:
    # Configure the server based on the mode
    modeConfig = get_configuration(ServerMode.HUB)
    start_grpc_hub(modeConfig, SLAVE_SERVERS)
