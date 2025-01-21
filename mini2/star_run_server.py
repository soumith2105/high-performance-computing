import sys
from src.utilities.modes import ModeConfiguration
import signal


# Central Hub
from src.star.grpc.central_hub import start_grpc_hub
from src.star.rest.central_hub import start_rest_hub

# Servers
from src.star.grpc.server import start_grpc_server
from src.star.rest.server import start_rest_server

hubConfig = ModeConfiguration(
    "HUB",
    "127.0.0.1:5000",
    None,
    None,
)


serverConfig = ModeConfiguration(
    "SERVER 1",
    "127.0.0.1:5000",
    None,
    None,
)

SLAVE_SERVERS = ["127.0.0.1:5001", "127.0.0.1:5002", "127.0.0.1:5003"]

# Register signal handler for graceful termination
signal.signal(signal.SIGINT, lambda x, y: sys.exit(1))
signal.signal(signal.SIGTERM, lambda x, y: sys.exit(1))


try:
    start_rest_hub(hubConfig, SLAVE_SERVERS)
    start_grpc_hub(hubConfig, SLAVE_SERVERS)

    start_rest_server(serverConfig)
    start_grpc_server(serverConfig)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

except KeyboardInterrupt:
    sys.exit(1)
