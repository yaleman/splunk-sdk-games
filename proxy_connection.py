""" testing a proxied connection to splunk """

from io import BytesIO

import urllib.request
import urllib
from typing import Any, Dict, List, Optional, Tuple, TypedDict
from splunklib import client  # type: ignore

import config

PROXY_HOST = "localhost"
PROXY_PORT = 3128


class RequestDict(TypedDict):
    """blep"""

    method: str
    headers: List[Tuple[str, Any]]
    body: str


# pylint: disable=too-few-public-methods
class ProxiedHandler:
    """blep"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        proxy_host: str,
        proxy_port: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        realm: Optional[str] = None,
    ) -> None:
        """setup"""
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.username = username
        self.password = password
        self.realm = realm

    def handler(self, url: str, request_dict: RequestDict) -> Dict[str, Any]:
        """handles connections"""
        headers = {
            "User-Agent": "splunk-sdk-python/1.7.2",
            "Accept": "*/*",
            "Connection": "Close",
        }
        for header in request_dict["headers"]:
            key, value = header
            headers[key] = value

        source_data = request_dict.get("body", "")
        if source_data == "":
            data = None
        elif isinstance(source_data, str):
            data = source_data.encode("utf-8")
        else:
            data = source_data

        req = urllib.request.Request(
            url,
            headers=headers,
            method= request_dict.get("method", "GET"),
        )
        proxy_handler = urllib.request.ProxyHandler(
            {
                "https": f"http://{self.proxy_host}:{self.proxy_port}/",
                "http": f"http://{self.proxy_host}:{self.proxy_port}/",
            },
        )

        if self.username is not None and self.realm is not None:
            proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
            proxy_auth_handler.add_password(self.realm, self.proxy_host, self.username, self.password)  # type: ignore
            opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
        else:
            # no-auth
            opener = urllib.request.build_opener(proxy_handler)

        with opener.open(req, data) as response:
            result = {
                "status": response.status,
                "headers": response.getheaders(),
                "body": BytesIO(response.read()),
                "reason": response.reason,
            }
            return result


proxyhandler = ProxiedHandler(
    proxy_host=PROXY_HOST,
    proxy_port=PROXY_PORT,
)

service = client.connect(
    host=config.host,
    username=config.username,
    password=config.password,
    autoLogin=True,
    handler=proxyhandler.handler,
)

print(service.info)
