from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis
import config as cfg
import jwt
import hashlib
import uuid

class Auth():
    """Microservice for user authentication"""
    # Vars

    name = 'auth'
    db = Redis('redis')
    logger_rpc = RpcProxy('logger')

   # Logic

    def _is_valid(self, login, password):
        """Checking login/password
        :returns: True if user is valid"""
        try:
            user_data = self.db.hgetall(login)
            salt = user_data['salt']
            input_hash = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
            return input_hash == user_data['hash']
        except:
            return False

   # API

    @rpc
    def register(self, login, password):
        """Computing hash and saving password into db"
        :returns: True if user was register and False otherwise"""
        self.logger_rpc.log(self.name, self.register.__name__, [login, password], "Info", "Registering")
        # Ensure that user is not already registered
        if self.db.hgetall(login) == {}:
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
            self.db.hmset(login, {
                'salt': salt,
                'hash': hashed_password
            })
            return True
        else:
            return False

    @rpc
    def login(self, login, password):
        """Logging in user, getting JWT
        :params: login, password
        :returns: JWT or False if user is not valid"""
        self.logger_rpc.log(self.name, self.login.__name__, [login, password], "Info", "Loggining")
        if self._is_valid(login, password):
            return jwt.encode({ 'login': login }, cfg.JWT_SECRET, cfg.JWT_ALGORITHM).decode('utf-8')    
        else:
            return False

    @rpc 
    def check_jwt(self, jwt_token):
        """Validating jwt
        :returns: user login and False if token is not valid"""
        self.logger_rpc.log(self.name, self.check_jwt.__name__, jwt_token, "Info", "Checking jwt")
        try:
            payload = jwt.decode(jwt_token, cfg.JWT_SECRET, algorithms=cfg.JWT_ALGORITHM)
        except jwt.DecodeError:
            return False
        return payload['login']

    @rpc 
    def get_all_logins(self):
        """Getting a list of all user logins
        :returns:
            keys - list of all logins"""
        self.logger_rpc.log(self.name, self.get_all_logins.__name__, None, "Info", "Getting all logins")
        return self.db.keys()
