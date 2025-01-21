from flask import Flask, request, jsonify
import requests
import logging
import time
import threading
from math import ceil

from src.utilities.colors import print_green, print_yellow, print_red, print_magenta
from src.utilities.modes import ModeConfiguration
from src.utilities.print_prefix import set_print_prefix


class RestServer:
    def __init__(self, modeConfig: ModeConfiguration, id: int):
        self.app = Flask(__name__)
        self.log = logging.getLogger("werkzeug")
        self.log.setLevel(logging.ERROR)

        self.HOST = modeConfig.self_url
        self.LEFT = modeConfig.left_url
        self.RIGHT = modeConfig.right_url
        self.SERVER_NAME = modeConfig.server_name
        self.ID = id

        self.TASK_QUEUE = []
        self.CURRENTLY_PROCESSING = None
        self.STEALING_IN_PROGRESS = 0

        self.LEFT_HOST_CONFIG = {"LEFT": None, "RIGHT": None, "TASK_QUEUE": []}

        self.RIGHT_HOST_CONFIG = {"LEFT": None, "RIGHT": None, "TASK_QUEUE": []}
        self.LEFT_RETRIES = 0
        self.RIGHT_RETRIES = 0

        set_print_prefix(self.SERVER_NAME)
        self.setup_routes()

    def get_url(self, server):
        return f"http://{server}/"

    def setup_routes(self):
        @self.app.route("/add_task", methods=["POST"])
        def add_task_to_queue():
            task = request.json
            self.TASK_QUEUE += task
            return jsonify({"status": "OK"}), 200

        @self.app.route("/heartbeat", methods=["POST"])
        def heartbeat_receive():
            URL, count = None, None
            if request.json["SELF"] == self.LEFT:
                self.LEFT_HOST_CONFIG = request.json
                if self.LEFT_HOST_CONFIG and self.RIGHT_HOST_CONFIG:
                    URL, count = self.steal_tasks(
                        len(self.LEFT_HOST_CONFIG["TASK_QUEUE"]),
                        len(self.TASK_QUEUE) + self.STEALING_IN_PROGRESS,
                        len(self.RIGHT_HOST_CONFIG["TASK_QUEUE"]),
                    )

            elif request.json["SELF"] == self.RIGHT:
                self.RIGHT_HOST_CONFIG = request.json
                if self.LEFT_HOST_CONFIG and self.RIGHT_HOST_CONFIG:
                    URL, count = self.steal_tasks(
                        len(self.LEFT_HOST_CONFIG["TASK_QUEUE"]),
                        len(self.TASK_QUEUE) + self.STEALING_IN_PROGRESS,
                        len(self.RIGHT_HOST_CONFIG["TASK_QUEUE"]),
                    )

            try:
                if count > 0 and URL:
                    print_green(f"Stealing {count} tasks from {URL}")
                    self.STEALING_IN_PROGRESS = count
                    response = requests.post(
                        self.get_url(URL) + "request_tasks", json=count
                    )
                    if response.status_code == 200:
                        tasks = response.json()
                        self.STEALING_IN_PROGRESS = 0
                        self.TASK_QUEUE += tasks

            except:
                self.STEALING_IN_PROGRESS = 0
                if URL == self.LEFT:
                    self.LEFT_RETRIES += 1
                elif URL == self.RIGHT:
                    self.RIGHT_RETRIES += 1

            return jsonify({"status": "OK"}), 200

        @self.app.route("/request_tasks", methods=["POST"])
        def request_tasks():
            count = request.json
            if count > 0 and len(self.TASK_QUEUE) > count:
                tasks = self.TASK_QUEUE[-count:]
                self.TASK_QUEUE = self.TASK_QUEUE[:-count]
                return jsonify(tasks), 200

            return jsonify([]), 200

    def steal_tasks(self, left_count, self_count, right_count):
        if left_count > self_count or right_count > self_count:
            mean = ceil((left_count + self_count + right_count) / 3)
            if left_count > mean:
                return self.LEFT, left_count - mean
            elif right_count > mean:
                return self.RIGHT, right_count - mean
        return None, 0

    def send_heartbeat_left(self):
        time.sleep(0.1 * self.ID)

        while True:
            time.sleep(3)
            try:
                requests.post(
                    self.get_url(self.LEFT) + "heartbeat",
                    json={
                        "LEFT": self.LEFT,
                        "SELF": self.HOST,
                        "RIGHT": self.RIGHT,
                        "TASK_QUEUE": self.TASK_QUEUE,
                    },
                )
                self.LEFT_RETRIES = 0

            except:
                print_red(f"Failed to send heartbeat to left: {self.LEFT}")
                self.LEFT_RETRIES += 1
                if self.LEFT_RETRIES >= 2:
                    self.LEFT = self.LEFT_HOST_CONFIG["LEFT"]
                    print_magenta(
                        f"Server {self.LEFT_HOST_CONFIG['LEFT']} dropped. {len(self.LEFT_HOST_CONFIG['TASK_QUEUE'])} tasks added to queue."
                    )
                    self.TASK_QUEUE += self.LEFT_HOST_CONFIG["TASK_QUEUE"]

    def send_heartbeat_right(self):
        time.sleep(0.1 * self.ID)

        while True:
            time.sleep(3)
            try:
                requests.post(
                    self.get_url(self.RIGHT) + "heartbeat",
                    json={
                        "LEFT": self.LEFT,
                        "SELF": self.HOST,
                        "RIGHT": self.RIGHT,
                        "TASK_QUEUE": self.TASK_QUEUE,
                    },
                )
                self.RIGHT_RETRIES = 0

            except:
                print_red(f"Failed to send heartbeat to right: {self.RIGHT}")
                self.RIGHT_RETRIES += 1
                if self.RIGHT_RETRIES >= 2:
                    self.RIGHT = self.RIGHT_HOST_CONFIG["RIGHT"]

    def log_status(self):
        while True:
            time.sleep(3 + (0.001 * self.ID))
            print_yellow(
                f"Task Queue: {len(self.TASK_QUEUE)},",
                f"Currently Processing: {self.CURRENTLY_PROCESSING['task'] if self.CURRENTLY_PROCESSING else None}",
            )

    def process_tasks(self):
        while True:
            if len(self.TASK_QUEUE) > 0 and self.CURRENTLY_PROCESSING is None:
                self.CURRENTLY_PROCESSING = self.TASK_QUEUE.pop(0)
                # print_yellow(f"Processing task: {self.CURRENTLY_PROCESSING['task']}")
                time.sleep(self.CURRENTLY_PROCESSING["timeout"])
                self.CURRENTLY_PROCESSING = None
            time.sleep(1)

    def run(self):
        threading.Thread(target=self.send_heartbeat_left, daemon=True).start()
        threading.Thread(target=self.send_heartbeat_right, daemon=True).start()
        threading.Thread(target=self.log_status, daemon=True).start()
        threading.Thread(target=self.process_tasks, daemon=True).start()
        self.app.run(port=int(self.HOST.split(":")[1]), debug=False)


def start_rest_server(modeConfig: ModeConfiguration, id: int) -> None:
    server = RestServer(modeConfig, id)
    server.run()


def start_rest_server_by_mode(modeConfig: ModeConfiguration, id: int) -> None:
    start_rest_server(modeConfig, id)
