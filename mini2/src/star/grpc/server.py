from typing import List
import grpc
from concurrent import futures
from src.process.ArrayOfObjects import ArrayOfObjects
from src.process.ObjectOfArrays import ObjectOfArrays
from src.utilities.colors import print_yellow
from src.utilities.modes import ModeConfiguration, ServerMode, get_configuration
from src.utilities.print_prefix import set_print_prefix
import src.star.grpc.star_service_pb2 as star_service_pb2
import src.star.grpc.star_service_pb2_grpc as star_service_pb2_grpc


class DataProcessor(star_service_pb2_grpc.DataProcessorServicer):
    def __init__(self, modeConfig: ModeConfiguration):
        self.HOST = modeConfig.self_url
        self.SERVER_NAME = modeConfig.server_name

        # Set server configurations
        set_print_prefix(self.SERVER_NAME)

    def ProcessData(self, request, context):
        print_yellow(f"Request received at Server: {request.message}")
        response = star_service_pb2.DataResponse(
            reply=f"Processed {request.message}",
        )
        return response

    def GetArrayOfObject(self, request, context):
        print_yellow(f"Request received at Server: {request.message}")
        obj = star_service_pb2.ArrayOfObjectResponse(
            object=[
                star_service_pb2.ArrayObject(
                    latitude=i["latitude"],
                    longitude=i["longitude"],
                    parameter=i["parameter"],
                    aqi=i["aqi"],
                    sitename=i["sitename"],
                )
                for i in ArrayOfObjects().read_dataset()
            ]
        )
        return obj

    def GetObjectOfArray(self, request, context):
        print_yellow(f"Request received at Server: {request.message}")
        data = ObjectOfArrays().read_dataset()
        obj = star_service_pb2.ObjectOfArrayResponse(
            latitude=data["latitude"],
            longitude=data["longitude"],
            parameter=data["parameter"],
            aqi=data["aqi"],
            sitename=data["sitename"],
        )
        return obj


def start_grpc_server(modeConfig: ModeConfiguration):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_obj = DataProcessor(modeConfig)
    star_service_pb2_grpc.add_DataProcessorServicer_to_server(server_obj, server)
    server.add_insecure_port(server_obj.HOST)
    server.start()
    print(f"Server {server_obj.HOST} is running...")
    server.wait_for_termination()


def start_grpc_server_by_mode(MODE: ServerMode) -> None:
    # Configure the server based on the mode
    modeConfig = get_configuration(MODE)
    start_grpc_server(modeConfig)
