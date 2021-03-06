import hashlib
import logging

from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.exceptions import UniqueUsernameException, ValidationPasswordException

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_REGISTER_CODE, MESSAGE_ACTION_REGISTER_LOGIN, \
    MESSAGE_ACTION_REGISTER_PASSWORD
from xserver.actionsserver.settings import MAX_USERNAME_LENGTH

logger = logging.getLogger("RegisterAction")


class RegisterAction(ActionBase):

    def __init__(self, message):
        super().__init__(message)

    def get_action_number(self):
        return MESSAGE_ACTION_REGISTER_CODE

    def execute(self):
        logger.debug("Executing REGISTER action started.")
        username = self.msg.get_body_param(MESSAGE_ACTION_REGISTER_LOGIN)
        password = self.msg.get_body_param(MESSAGE_ACTION_REGISTER_PASSWORD)

        if not self._check_username_length(username):
            self.set_error_with_status("Given name is too long. Maximal length = " + str(MAX_USERNAME_LENGTH))
            return

        # Check if user with such nick does not already exists
        with self.db_connect as cursor:
            try:
                self._is_username_unique(username, cursor)
                self._validate_password(password)
                self._insert_new_user_to_db(username, password, cursor)
            except (UniqueUsernameException, ValidationPasswordException) as e:
                self.set_error_with_status(e.message)
                return

        self.set_status_ok()
        logger.debug("Action REGISTER executed SUCCESSFULLY.")

    def _is_username_unique(self, username, cursor):
        query = "SELECT * FROM users_user WHERE username='{}'"

        logger.debug("Executing query: " + query + "\n\twith params: " + str((username,)))

        cursor.execute(query.format(username))
        result = cursor.fetchone()
        logger.debug("Query result: " + str(result))

        if result:
            logger.debug("Inserted username is not unique.")
            raise UniqueUsernameException()
        return cursor.fetchone() is None

    def _check_username_length(self, username):
        return True if len(username) < MAX_USERNAME_LENGTH else False

    def _validate_password(self, passwd):
        if len(passwd) > 5:
            return True
        logger.debug("User's password is too weak.")
        raise ValidationPasswordException()

    def _get_user_password_hash(self, password):
        hash_alg = hashlib.sha3_256()
        hash_alg.update(password.encode())
        return hash_alg.hexdigest()

    def _insert_new_user_to_db(self, username, password, cursor):
        query = "INSERT INTO users_user (username, password) VALUES ('{}', '{}')"

        hash_pass = self._get_user_password_hash(password)

        logger.debug("Executing query: " + query + "\n\twith params: " + str((username, hash_pass)))

        cursor.execute(query.format(username, hash_pass))
        self.db_connect.connection.commit()
        logger.debug("Query executed successfully.")
