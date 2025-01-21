from flask import Flask, request, jsonify
import requests
import time
from typing import List
import logging

from src.utilities.colors import print_blue
from src.utilities.modes import ModeConfiguration, ServerMode, get_configuration
from src.utilities.print_prefix import set_print_prefix


def start_rest_hub(modeConfig: ModeConfiguration, SLAVE_SERVERS: List[str]) -> None:
    app = Flask(__name__)

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    HOST = modeConfig.self_url
    SERVER_NAME = modeConfig.server_name

    # Set server configurations
    set_print_prefix(SERVER_NAME)

    def get_url(server):
        return f"http://{server}"

    @app.route("/process", methods=["POST"])
    def process_request():
        data = request.get_json()
        target = data.get("target")
        if not target or target not in SLAVE_SERVERS:
            print("Invalid or missing target slave")
            return jsonify({"error": "Invalid or missing target slave"}), 400

        print_blue(f"Routing message '{data['message']}' to {target}")
        response = requests.post(f"{get_url(target)}/process", json=data)
        return jsonify(response.json()), response.status_code

    app.run(port=int(HOST.split(":")[1]), debug=False)


def start_rest_hub_by_mode(*SLAVE_SERVERS: List[str]) -> None:
    modeConfig = get_configuration(ServerMode.HUB)
    start_rest_hub(modeConfig, SLAVE_SERVERS)
