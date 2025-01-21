import grpc
from concurrent import futures
from src.process.ArrayOfObjects import ArrayOfObjects
from src.process.ObjectOfArrays import ObjectOfArrays
import src.ring.grpc.ring_pb2 as ring_pb2
import src.ring.grpc.ring_pb2_grpc as ring_pb2_grpc
from src.utilities.colors import print_green, print_yellow
from src.utilities.modes import (
    ServerMode,
    ServerURLS,
    get_configuration,
    ModeConfiguration,
)
from src.utilities.print_prefix import set_print_prefix


class RingServerService(ring_pb2_grpc.RingServerServicer):
    def __init__(self, modeConfig: ModeConfiguration):
        self.HOST = modeConfig.self_url
        self.LEFT = modeConfig.left_url
        self.RIGHT = modeConfig.right_url
        self.SERVER_NAME = modeConfig.server_name
        # Set server configurations
        set_print_prefix(self.SERVER_NAME)

    def Relay(self, request, context):
        if request.target == self.HOST:
            print_green(f"Message delivered to {self.HOST}: {request.message}")
            return ring_pb2.Response(
                message=f"Message '{request.message}' received at {self.HOST}",
                success=True,
            )

        next_hop = self.RIGHT if request.target in self.RIGHT else self.LEFT
        print_yellow(f"Relaying message from {self.HOST} to {next_hop}")
        with grpc.insecure_channel(next_hop) as channel:
            stub = ring_pb2_grpc.RingServerStub(channel)
            return stub.Relay(request)

    def Register(self, request, context):
        print_yellow(f"Received registration request -> Relaying to {self.RIGHT}")

        if self.RIGHT == ServerURLS.HUB:
            with grpc.insecure_channel(self.RIGHT) as channel:
                stub = ring_pb2_grpc.CentralHubStub(channel)
                response = stub.Register(
                    ring_pb2.RingResponse(
                        ring={
                            **request.ring,
                            self.HOST: ring_pb2.Node(left=self.LEFT, right=self.RIGHT),
                        }
                    )
                )
                return response
        else:
            with grpc.insecure_channel(self.RIGHT) as channel:
                stub = ring_pb2_grpc.RingServerStub(channel)
                response = stub.Register(
                    ring_pb2.RingResponse(
                        ring={
                            **request.ring,
                            self.HOST: ring_pb2.Node(left=self.LEFT, right=self.RIGHT),
                        }
                    )
                )
                return response

    def GetArrayOfObject(self, request, context):
        if request.target == self.HOST:
            print_green(f"Message delivered to {self.HOST}: {request.message}")
            obj = ring_pb2.ArrayOfObjectResponse(
                object=[
                    ring_pb2.ArrayObject(
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

        next_hop = self.RIGHT if request.target in self.RIGHT else self.LEFT
        print_yellow(f"Relaying message from {self.HOST} to {next_hop}")
        with grpc.insecure_channel(
            next_hop,
            options=[("grpc.max_receive_message_length", 1024 * 1024 * 1024)],
        ) as channel:
            stub = ring_pb2_grpc.RingServerStub(channel)
            return stub.GetArrayOfObject(request)

    def GetObjectOfArray(self, request, context):
        if request.target == self.HOST:
            print_green(f"Message delivered to {self.HOST}: {request.message}")
            data = ObjectOfArrays().read_dataset()
            obj = ring_pb2.ObjectOfArrayResponse(
                latitude=data["latitude"],
                longitude=data["longitude"],
                parameter=data["parameter"],
                aqi=data["aqi"],
                sitename=data["sitename"],
            )
            return obj

        next_hop = self.RIGHT if request.target in self.RIGHT else self.LEFT
        print_yellow(f"Relaying message from {self.HOST} to {next_hop}")
        with grpc.insecure_channel(
            next_hop,
            options=[("grpc.max_receive_message_length", 1024 * 1024 * 1024)],
        ) as channel:
            stub = ring_pb2_grpc.RingServerStub(channel)
            return stub.GetObjectOfArray(request)


def start_grpc_server(modeConfig: ModeConfiguration):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_obj = RingServerService(modeConfig)
    ring_pb2_grpc.add_RingServerServicer_to_server(server_obj, server)
    server.add_insecure_port(server_obj.HOST)
    server.start()
    print(f"Server {server_obj.HOST} is running...")
    server.wait_for_termination()


def start_grpc_server_by_mode(MODE: ServerMode) -> None:
    # Configure the server based on the mode
    modeConfig = get_configuration(MODE)
    start_grpc_server(modeConfig)
