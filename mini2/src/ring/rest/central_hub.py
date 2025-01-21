from flask import Flask, request, jsonify
import sys
import requests
import logging

from src.utilities.print_prefix import set_print_prefix
from src.utilities.hub_functions import find_shortest_path, print_ring
from src.utilities.modes import get_configuration, ServerMode, ModeConfiguration
from src.utilities.colors import print_yellow, print_blue


def start_rest_hub(modeConfig: ModeConfiguration) -> None:

    app = Flask(__name__)

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    SERVER_MAP = {}

    HOST = modeConfig.self_url
    LEFT = modeConfig.left_url
    RIGHT = modeConfig.right_url
    SERVER_NAME = modeConfig.server_name

    # Set server configurations
    set_print_prefix(SERVER_NAME)

    def get_url(server):
        return f"http://{server}"

    @app.route("/discover", methods=["GET"])
    def discover_servers():
        """
        Initiates discovery of servers and establishes the ring topology.
        """
        print_yellow(f"Sending ping to " + RIGHT)
        data = {HOST: {"right": RIGHT, "left": LEFT}}
        response = requests.post(get_url(RIGHT) + "/register", json=data)
        return jsonify(response.json()), response.status_code

    @app.route("/register", methods=["POST"])
    def register():
        """
        Handles registration of servers and updates SERVER_MAP with the topology.
        """
        data = request.get_json()
        SERVER_MAP.update(data)
        keys = {k: SERVER_MAP[k]["left"] for k in SERVER_MAP}
        print_ring(keys, HOST)
        return {"success": True}, 200

    @app.route("/send_message", methods=["POST"])
    def send_message():
        """
        Handles client requests to send a message to a specific server and returns its response.
        """
        data = request.get_json()
        target = data.get("target")
        message = data.get("message")

        if target not in SERVER_MAP:
            return {"error": "Target server not found"}, 404

        # Determine the shortest path
        path = find_shortest_path(target=target, host=HOST, server_map=SERVER_MAP)
        print_blue(f"Routing message '{message}' to {target} via {path}")

        # Send the message to the target server and wait for the response
        response = requests.post(
            get_url(path) + "/relay_message",
            json={"target": target, "message": message},
        )
        return jsonify(response.json()), response.status_code

    app.run(port=int(HOST.split(":")[1]), debug=False)


def start_rest_hub_by_mode() -> None:
    modeConfig = get_configuration(ServerMode.HUB)
    start_rest_hub(modeConfig)
