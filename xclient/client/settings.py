import os

BASE_HEADERS = {
    'ConLen': '',
    'Token': '',
    'Action': '',
}

CLIENT_SEND_ACTIONS = {
    'login': 1,
    'register': 2,
    'create_room': 3,
    'join_room': 4,
    'list_rooms': 5,
    'leave_room': 6,
    'list_user': 7,
    'send_message': 8,
    'logout': 9,
}

RECEIVE_MESSAGE_CODE = 10

TOKEN_KEY = 'Token'
STATUS_KEY = 'Status'

RESPONSE_ACTION_HEADER = 'Action'
RESPONSE_TOKEN_KEY = 'Token'

SUCCESS_RESPONSES = ['ok', ]
TLS = True
ROOT_PATH = os.path.dirname(__file__)
CERT_PATH = os.path.join(ROOT_PATH,'client.crt')
KEY_PATH = os.path.join(ROOT_PATH, 'client.key')
SERVER_CERT = os.path.abspath('../../xserver/coreserver/server.cert')

