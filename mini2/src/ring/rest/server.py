from flask import Flask, request, jsonify
import sys
import requests
import logging
import os

from src.process.ArrayOfObjects import ArrayOfObjects
from src.process.ObjectOfArrays import ObjectOfArrays
from src.utilities.colors import print_green, print_yellow
from src.utilities.modes import get_configuration, ModeConfiguration, ServerMode
from src.utilities.print_prefix import set_print_prefix


def start_rest_server(modeConfig: ModeConfiguration) -> None:

    app = Flask(__name__)

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    HOST = modeConfig.self_url
    LEFT = modeConfig.left_url
    RIGHT = modeConfig.right_url
    SERVER_NAME = modeConfig.server_name

    # Set server configurations
    set_print_prefix(SERVER_NAME)

    def get_url(server):
        return f"http://{server}"

    @app.route("/relay_message", methods=["POST"])
    def handle_relay_message():
        """
        Handles relayed messages and forwards them if necessary.
        """
        data = request.get_json()
        target = data.get("target")
        message = data.get("message")

        if target == HOST:
            print_green(f"Message delivered to {HOST}: {message}")
            obj = (
                ObjectOfArrays().read_dataset()
            )  # Change this line to ArrayOfObjects to test the other method
            return {"response": obj}, 200

        # Relay the message to the next server
        next_hop = RIGHT if target in RIGHT else LEFT
        print_yellow(f"Relaying message from {HOST} to {next_hop}")
        return requests.post(
            get_url(next_hop) + "/relay_message",
            json={"target": target, "message": message},
        ).json()

    @app.route("/register", methods=["POST"])
    def register():
        """
        Updates the SERVER_MAP and forwards registration info in the ring.
        """
        data = request.get_json()
        print_yellow(
            f"Received registration request from {request.host_url} -> Relaying to {RIGHT}"
        )
        data.update({HOST: {"left": LEFT, "right": RIGHT}})
        response = requests.post(get_url(RIGHT) + "/register", json=data)
        return jsonify(response.json()), response.status_code

    app.run(port=int(HOST.split(":")[1]), debug=False)


def start_rest_server_by_mode(MODE: ServerMode) -> None:
    # Configure the server based on the mode
    modeConfig = get_configuration(MODE)
    start_rest_server(modeConfig)
