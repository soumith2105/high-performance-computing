from flask import Flask, request, jsonify
import logging

from src.utilities.colors import print_yellow
from src.utilities.modes import ModeConfiguration, ServerMode, get_configuration
from src.utilities.print_prefix import set_print_prefix
from src.process.ArrayOfObjects import ArrayOfObjects
from src.process.ObjectOfArrays import ObjectOfArrays


def start_rest_server(modeConfig: ModeConfiguration) -> None:
    app = Flask(__name__)

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    HOST = modeConfig.self_url
    SERVER_NAME = modeConfig.server_name

    # Set server configurations
    set_print_prefix(SERVER_NAME)

    @app.route("/process", methods=["POST"])
    def process():
        data = request.get_json()
        print_yellow(f"Request received at Server: {data['message']}")
        obj = (
            ObjectOfArrays().read_dataset()
        )  # Change this line to ArrayOfObjects to test the other method
        return {"success": obj}, 200

    app.run(port=int(HOST.split(":")[1]), debug=False)


def start_rest_server_by_mode(MODE: ServerMode) -> None:
    # Configure the server based on the mode
    modeConfig = get_configuration(MODE)
    start_rest_server(modeConfig)
