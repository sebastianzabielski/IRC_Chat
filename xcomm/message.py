from xcomm.xcomm_moduledefs import MESSAGE_CONTENT_LENGTH
from xcomm.settings import DELIMITER_BYTE, DELIMITER_STR, PARAM_VALUE_SEPARATOR


class Message:
    def __init__(self, header=None, body=None):
        self.header = {} if not header else header
        self.body = {} if not body else body

    def set_header_bytes(self, header_bytes):
        self.__parse_bytes(header_bytes, self.header)

    def get_header_param(self, param):
        return self.header.get(param, "")

    def add_header_param(self, param, value):
        self.header[param] = value

    def set_body_bytes(self, body_bytes):
        self.__parse_bytes(body_bytes, self.body)

    def get_body_param(self, param):
        return self.body.get(param, "")

    def add_body_param(self, param, value):
        self.body[param] = value

    # destination must be self.header or self.body
    def __parse_bytes(self, msg_bytes, destination):
        for item in filter(lambda x: len(x), msg_bytes.split(DELIMITER_BYTE)):
            split = item.decode().split(PARAM_VALUE_SEPARATOR, maxsplit=1)
            destination[split[0]] = split[1]

    def convert_message_to_bytes(self):
        return self.get_complete_message().encode()

    def get_complete_message(self):
        complete_body = ""
        for param, value in self.body.items():
            complete_body += f"{param}{PARAM_VALUE_SEPARATOR}{value}{DELIMITER_STR}"

        complete = MESSAGE_CONTENT_LENGTH + PARAM_VALUE_SEPARATOR + str(len(complete_body.encode())) + DELIMITER_STR

        for param, value in self.header.items():
            complete += f"{param}{PARAM_VALUE_SEPARATOR}{value}{DELIMITER_STR}"

        complete += DELIMITER_STR
        complete += complete_body
        return complete

    @staticmethod
    def from_bytes(bytes_msg):
        new_msg = Message()
        splitted = bytes_msg.split(DELIMITER_BYTE * 2)
        new_msg.set_header_bytes(splitted[0])
        new_msg.set_body_bytes(splitted[1])

        return new_msg
