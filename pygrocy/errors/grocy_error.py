from requests import Response


class GrocyError(Exception):
    def __init__(self, response: Response):
        self._status_code = response.status_code

        if len(response.text) > 0:
            json = response.json()
            self._message = json["error_message"]
        else:
            self._message = None

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message

    @property
    def is_client_error(self) -> bool:
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        return self.status_code >= 500
