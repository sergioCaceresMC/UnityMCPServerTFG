import json
import socket
import threading
import uuid
import os

from dotenv import load_dotenv
load_dotenv()

class UnityBridge:
    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
    ):
        self.host = host or os.getenv("UNITY_HOST", "127.0.0.1")
        self.port = port or int(os.getenv("UNITY_PORT", "8765"))
        self.connection = None
        self.reader = None

        self.lock = threading.Lock()

        self.connected = threading.Event()

    def start(self):
        thread = threading.Thread(
            target=self._server_loop,
            daemon=True
        )

        thread.start()

    def _server_loop(self):
        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        server.bind(
            (self.host, self.port)
        )

        server.listen(1)

        print(
            f"Waiting for Unity on "
            f"{self.host}:{self.port}"
        )

        while True:

            connection, address = server.accept()

            print(
                f"Unity connected from {address}"
            )

            self.connection = connection

            self.reader = connection.makefile(
                "r",
                encoding="utf-8"
            )

            self.connected.set()

    def call(
        self,
        command: str,
        args: dict | None = None
    ):

        if not self.connected.wait(timeout=5):
            raise RuntimeError(
                "Unity is not connected"
            )

        request_id = str(uuid.uuid4())

        message = {
            "id": request_id,
            "command": command,
            "args": args or {}
        }

        data = (
            json.dumps(message)
            + "\n"
        ).encode("utf-8")

        
        # Solo dejamos una llamada simultánea
        with self.lock:

            self.connection.sendall(data)

            while True:

                line = self.reader.readline()

                if not line:
                    self.connected.clear()

                    raise RuntimeError(
                        "Unity disconnected"
                    )

                response = json.loads(line)

                if response.get("id") == request_id:
                    break

        if not response.get("success"):
            raise RuntimeError(
                response.get(
                    "error",
                    "Unknown Unity error"
                )
            )

        return response["result"]
