from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseConnection:
    def __init__(self):
        self.engine = None
        self.session = None
        self.__PARAM_SCHEMA_DB_CONN = {
            "engine": str,
            "host": str,
            "name": str,
            "user": str,
            "passwd": str,
            "connect_args": dict,
            "auto_commit": bool,
            "auto_flush": bool,
            "expire_on_commit": bool,
        }

    def __validate_params(self, params, kwargs):
        for key, expected_type in params.items():
            if key in kwargs and not isinstance(kwargs[key], expected_type):
                raise TypeError(f"'{key}' must be of type {expected_type.__name__}")

    def __set_engine(self, **kwargs):
        uri = f"{kwargs.get('engine', None)}://{kwargs.get('user', None)}:{kwargs.get('passwd', None)}@{kwargs.get('host', None)}/{kwargs.get('name', None)}"
        self.engine = create_engine(uri, connect_args=kwargs.get("connect_args", None))

    def __set_session(self, auto_commit, auto_flush, expire_on_commit):
        if self.engine is None:
            raise ConnectionError("Database Engine Not Connected.")
        self.session = sessionmaker(
            bind=self.engine,
            autocommit=auto_commit,
            autoflush=auto_flush,
            expire_on_commit=expire_on_commit,
        )

    def connect(self, **kwargs):
        self.__validate_params(self.__PARAM_SCHEMA_DB_CONN, kwargs)
        self.__set_engine(**kwargs)
        self.__set_session(
            kwargs.get("auto_commit", None),
            kwargs.get("auto_flush", None),
            kwargs.get("expire_on_commit", None),
        )
