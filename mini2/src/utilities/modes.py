from enum import Enum


class ModeConfiguration:
    def __init__(self, server_name: str, self_url: str, left_url: str, right_url: str):
        self.server_name = server_name
        self.self_url = self_url
        self.left_url = left_url
        self.right_url = right_url


class ServerMode:
    HUB = "HUB"
    SERVER1 = "SERVER1"
    SERVER2 = "SERVER2"
    SERVER3 = "SERVER3"


class ServerURLS:
    HUB = "127.0.0.1:5000"
    SERVER1 = "127.0.0.1:5001"
    SERVER2 = "127.0.0.1:5002"
    SERVER3 = "127.0.0.1:5003"


HUB = ModeConfiguration(
    ServerMode.HUB, ServerURLS.HUB, ServerURLS.SERVER3, ServerURLS.SERVER1
)
SERVER1 = ModeConfiguration(
    ServerMode.SERVER1, ServerURLS.SERVER1, ServerURLS.HUB, ServerURLS.SERVER2
)
SERVER2 = ModeConfiguration(
    ServerMode.SERVER2, ServerURLS.SERVER2, ServerURLS.SERVER1, ServerURLS.SERVER3
)
SERVER3 = ModeConfiguration(
    ServerMode.SERVER3, ServerURLS.SERVER3, ServerURLS.SERVER2, ServerURLS.HUB
)


def get_configuration(server_name: ServerMode) -> ModeConfiguration:
    if server_name == ServerMode.SERVER1:
        return SERVER1
    elif server_name == ServerMode.SERVER2:
        return SERVER2
    elif server_name == ServerMode.SERVER3:
        return SERVER3
    elif server_name == ServerMode.HUB:
        return HUB
    else:
        raise ValueError(f"Invalid server mode: {server_name}")
