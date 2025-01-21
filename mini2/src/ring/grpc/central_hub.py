import grpc
from concurrent import futures
import src.ring.grpc.ring_pb2 as ring_pb2
import src.ring.grpc.ring_pb2_grpc as ring_pb2_grpc

from src.utilities.hub_functions import find_shortest_path, print_ring
from src.utilities.colors import print_yellow, print_blue
from src.utilities.modes import (
    ServerMode,
    ServerURLS,
    get_configuration,
    ModeConfiguration,
)
from src.utilities.print_prefix import set_print_prefix


class CentralHubService(ring_pb2_grpc.CentralHubServicer):
    def __init__(self, modeConfig: ModeConfiguration):
        self.SERVER_MAP = {}
        self.HOST = modeConfig.self_url
        self.LEFT = modeConfig.left_url
        self.RIGHT = modeConfig.right_url
        self.SERVER_NAME = modeConfig.server_name
        # Set server configurations
        set_print_prefix(self.SERVER_NAME)

    def Discover(self, request, context):
        """Initiates discovery of servers and establishes the ring topology."""
        print_yellow(f"Sending ping to {self.RIGHT}")
        self.SERVER_MAP[self.HOST] = {"right": self.RIGHT, "left": self.LEFT}
        # Forward register request to the right server
        with grpc.insecure_channel(self.RIGHT) as channel:
            stub = ring_pb2_grpc.RingServerStub(channel)
            obj = ring_pb2.RingResponse(
                ring={self.HOST: ring_pb2.Node(left=self.LEFT, right=self.RIGHT)}
            )
            response = stub.Register(obj)
            return response

    def Register(self, request, context):
        self.SERVER_MAP = {
            k: {"left": request.ring[k].left, "right": request.ring[k].right}
            for k in request.ring
        }
        print_ring({k: self.SERVER_MAP[k]["right"] for k in self.SERVER_MAP}, self.HOST)
        return ring_pb2.Response(message="Registered successfully", success=True)

    def SendMessage(self, request, context):
        if request.target not in self.SERVER_MAP:
            return ring_pb2.Response(message="Target server not found", success=False)

        path = find_shortest_path(
            target=request.target, host=self.HOST, server_map=self.SERVER_MAP
        )
        print_blue(
            f"Routing message '{request.message}' to {request.target} via {path}"
        )

        # Forward the message to the next server
        with grpc.insecure_channel(path) as channel:
            stub = ring_pb2_grpc.RingServerStub(channel)
            response = stub.Relay(request)
            return response

    def GetArrayOfObject(self, request, context):
        if request.target not in self.SERVER_MAP:
            return ring_pb2.Response(message="Target server not found", success=False)

        path = find_shortest_path(
            target=request.target, host=self.HOST, server_map=self.SERVER_MAP
        )
        print_blue(
            f"Routing message '{request.message}' to {request.target} via {path}"
        )

        # Forward the message to the next server
        with grpc.insecure_channel(
            path,
            options=[("grpc.max_receive_message_length", 1024 * 1024 * 1024)],
        ) as channel:
            stub = ring_pb2_grpc.RingServerStub(channel)
            response = stub.GetArrayOfObject(request)
            return response

    def GetObjectOfArray(self, request, context):
        if request.target not in self.SERVER_MAP:
            return ring_pb2.Response(message="Target server not found", success=False)

        path = find_shortest_path(
            target=request.target, host=self.HOST, server_map=self.SERVER_MAP
        )
        print_blue(
            f"Routing message '{request.message}' to {request.target} via {path}"
        )

        # Forward the message to the next server
        with grpc.insecure_channel(
            path,
            options=[("grpc.max_receive_message_length", 1024 * 1024 * 1024)],
        ) as channel:
            stub = ring_pb2_grpc.RingServerStub(channel)
            response = stub.GetObjectOfArray(request)
            return response


def start_grpc_hub(modeConfig: ModeConfiguration):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_send_message_length", 1024 * 1024 * 1024),  # 10 MB
            ("grpc.max_receive_message_length", 1024 * 1024 * 1024),  # 10 MB
        ],
    )
    ring_pb2_grpc.add_CentralHubServicer_to_server(
        CentralHubService(modeConfig), server
    )
    server.add_insecure_port(
        str(ServerURLS.HUB),
    )
    server.start()
    print("Central Hub is running...")
    server.wait_for_termination()


def start_grpc_hub_by_mode() -> None:
    # Configure the server based on the mode
    modeConfig = get_configuration(ServerMode.HUB)
    start_grpc_hub(modeConfig)
