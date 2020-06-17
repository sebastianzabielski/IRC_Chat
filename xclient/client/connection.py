import socket
import ssl

from xclient.client.settings import TLS, CERT_PATH, SERVER_CERT, KEY_PATH
from xclient.client.utils import Receiver
from xcomm.message import Message
from xcomm.xcomm_moduledefs import MESSAGE_CONTENT_LENGTH


class Connection:
    def __init__(self, ip, port, client):
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        self.client = client

    def __enter__(self):
        self.socket.connect((self.ip, self.port))
        if TLS:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self.context.verify_mode = ssl.CERT_REQUIRED
            self.context.load_verify_locations(SERVER_CERT)
            self.context.load_cert_chain(certfile=CERT_PATH, keyfile=KEY_PATH)
            self.secure_socket = self.context.wrap_socket(self.socket, server_side=False, server_hostname=self.ip)

        return self

    def get_socket(self):
        return self.secure_socket if TLS else self.socket

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client.token:
            self.client.logout()
        print(exc_type, exc_val, exc_tb)

        if TLS:
            self.secure_socket.close()
        self.socket.close()

    def send(self, message: Message):
        sock = self.get_socket()
        return sock.sendall(message.convert_message_to_bytes())

    def receive(self):
        sock = self.get_socket()
        m = Message()
        headers = Receiver.receive_headers(sock)
        m.set_header_bytes(headers)
        content_length = m.get_header_param(MESSAGE_CONTENT_LENGTH)
        body = Receiver.receive_body(sock, content_length)
        m.set_body_bytes(body)
        return m
