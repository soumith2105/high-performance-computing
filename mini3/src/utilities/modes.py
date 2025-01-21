from enum import Enum


class ModeConfiguration:
    def __init__(self, server_name: str, self_url: str, left_url: str, right_url: str):
        self.server_name = server_name
        self.self_url = self_url
        self.left_url = left_url
        self.right_url = right_url
