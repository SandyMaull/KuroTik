import redis
import json


class KuroTikRedis:
    def __init__(self):
        self.__PARAM_SCHEMA_REDIS = {
            "host": str,
            "port": int,
            "db": int,
            "username": str,
            "password": str,
        }
        self.conn = None

    def __validate_params(self, params, kwargs, check_conn=True):
        if check_conn and self.conn is None:
            raise ConnectionError("Redis Not Connected.")
        for key, expected_type in params.items():
            if key in kwargs and not isinstance(kwargs[key], expected_type):
                raise TypeError(f"'{key}' must be of type {expected_type.__name__}")

    def connect(self, **kwargs):
        self.__validate_params(self.__PARAM_SCHEMA_REDIS, kwargs, False)
        self.conn = redis.Redis(
            host=kwargs.get("host", None),
            port=kwargs.get("port", 6379),
            db=kwargs.get("db", 0),
            username=kwargs.get("username", None),
            password=kwargs.get("password", None),
        )

    def getDataR(self, key):
        cached = self.conn.get(key)
        return json.loads(cached) if cached else None

    def setDataR(self, key, data):
        self.conn.set(key, json.dumps(data), ex=300)
        return self.getDataR(key)
