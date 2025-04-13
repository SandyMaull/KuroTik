# ==============================================================================
#  ©2025 Kuronekosan. All Rights Reserved.
#
#  Packages:    kurotik
#  Author:      Kuronekosan
#  Created:     2025
#
#  Description:
#      A Custom Mikrotik Packages for automatic enabled/disabled block script
# ==============================================================================

from routeros_api import RouterOsApiPool


class KuroTik:
    def __init__(self):
        self.__PARAM_SCHEMA_MKT_CONN = {
            "host": str,
            "username": str,
            "password": str,
            "port": int,
            "plaintext_login": bool,
            "use_ssl": bool,
            "ssl_verify": bool,
            "ssl_verify_hostname": bool,
            "ssl_context": any,
        }
        self.__PARAM_SCHEMA_MKT_EXEC = {
            "x": str,
            "resources": str,
            "function": str,
            "params": dict,
        }
        self.conn = None
        self.api = None

    def __validate_params(self, params, kwargs, check_conn=True):
        if check_conn and self.conn is None:
            raise ConnectionError("Mikrotik API Not Connected.")
        for key, expected_type in params.items():
            if key in kwargs and not isinstance(kwargs[key], expected_type):
                raise TypeError(f"'{key}' must be of type {expected_type.__name__}")

    def __setConnection(self, **kwargs):
        self.__validate_params(self.__PARAM_SCHEMA_MKT_CONN, kwargs, False)
        self.conn = RouterOsApiPool(
            host=kwargs.get("host", ""),
            username=kwargs.get("username", "admin"),
            password=kwargs.get("password", ""),
            port=kwargs.get("port", 8728),
            plaintext_login=kwargs.get("plaintext_login", False),
            use_ssl=kwargs.get("use_ssl", False),
            ssl_verify=kwargs.get("ssl_verify", False),
            ssl_verify_hostname=kwargs.get("ssl_verify_hostname", False),
            ssl_context=kwargs.get("ssl_context", None),
        )
        self.api = self.conn.get_api()

    def __executeCommands(self, **kwargs):
        self.__validate_params(self.__PARAM_SCHEMA_MKT_EXEC, kwargs)
        if kwargs.get("x", None):
            return self.api.get_resource(kwargs["x"])
        return self.api.get_resource(kwargs.get("resources", "/")).call(
            kwargs.get("function", "ping"),
            kwargs.get("params", {"address": "8.8.8.8", "count": "4"}),
        )

    def connect(self, **kwargs):
        """
        Create a connection to mikrotik API.

        Required Keyword Args:
            host (str): Hostname or IP mikrotik,
            username (str): Username mikrotik,
            password (str): Password mikrotik
        Additional Keyword Args:
            port (int): Port Mikrotik,
            plaintext_login (bool): Set type of login,
            use_ssl (bool): Set SSL for interactions,
            ssl_verify (bool): Set Verify SSL for interactions,
            ssl_verify_hostname (bool): Set Hostname of Verify SSL,
            ssl_context (any): Any SSL context,
        """
        self.__setConnection(**kwargs)
        return self.api

    def execute(self, **kwargs):
        """
        Execute a command to mikrotik API.

        Additional Keyword Args:
            x (str): Use this if u want to directly execute command without any resources/function (need method chaining after),
            resources (str): Set resources of the command,
            function (str): Set function of the command,
            params (dict): Set params of the command

        Example Use:
            - test.execute(x='/queue/simple').get()
            - test.execute(resources='/', function='ping', params={'address': '8.8.8.8', 'count': '4'})
        """
        return self.__executeCommands(**kwargs)
