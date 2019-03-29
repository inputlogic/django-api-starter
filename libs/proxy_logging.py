import requests
import socket
from rest_framework_tracking.mixins import LoggingMixin


class ProxyLoggingMixin(LoggingMixin):
    def __get_server_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't have to be reachable
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def __get_server_hostname(self):
        try:
            hostname = socket.gethostname()
        except Exception:
            hostname = 'localhost'
        return hostname

    def with_log(self, parent_request, method, path, headers, body, params=None):
        prepared_request = requests.Request(
            method, path, params=params, headers=headers, json=body
        ).prepare()

        response = requests.get(path, headers=headers, json=body, params=params)

        self.log_proxy_response(parent_request, prepared_request, body, response)
        return response

    def log_proxy_response(self, request, prepared_request, body, response):
        import urllib.parse as urlparse
        parsed = urlparse.urlparse(prepared_request.url)

        self.log.update(
            {
                'remote_addr': self.__get_server_ip(),
                'view': self._get_view_name(request),
                'view_method': self._get_view_method(prepared_request),
                'path': '(via proxy) ' + prepared_request.url,
                'host': self.__get_server_hostname(),
                'method': prepared_request.method,
                'query_params': parsed.query,
                'user': self._get_user(request),
                'response_ms': self._get_response_ms(),
                'response': self._clean_data(response.content.decode("utf-8")),
                'status_code': response.status_code,
                'data': body
            }
        )

        self.handle_log()
        return response
