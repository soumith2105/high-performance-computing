import sys
from src.utilities.modes import ModeConfiguration
import signal


# Central Hub
from src.ring.grpc.central_hub import start_grpc_hub
from src.ring.rest.central_hub import start_rest_hub

# Servers
from src.ring.grpc.server import start_grpc_server
from src.ring.rest.server import start_rest_server

hubConfig = ModeConfiguration(
    "HUB",
    "127.0.0.1:5000",
    "127.0.0.1:5001",
    "127.0.0.1:5002",
)


serverConfig = ModeConfiguration(
    "SERVER 1",
    "127.0.0.1:5000",
    "127.0.0.1:5001",
    "127.0.0.1:5002",
)

# Register signal handler for graceful termination
signal.signal(signal.SIGINT, lambda x, y: sys.exit(1))
signal.signal(signal.SIGTERM, lambda x, y: sys.exit(1))


try:
    start_rest_hub(hubConfig)
    start_grpc_hub(hubConfig)

    start_rest_server(serverConfig)
    start_grpc_server(serverConfig)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

except KeyboardInterrupt:
    sys.exit(1)
