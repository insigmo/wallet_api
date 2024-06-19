import logging
import textwrap
from urllib.parse import urljoin

from requests import HTTPError, Response
from requests_toolbelt.sessions import BaseUrlSession


class HttpClient(BaseUrlSession):
    @staticmethod
    def join_url(base_url: str, url: str) -> str:
        url = url.lstrip('/')
        if not base_url.endswith('/'):
            base_url += '/'

        return urljoin(base_url, url)

    def request(self, method: str, url: str, *args, **kwargs) -> Response:
        url = self.join_url(self.base_url, url)
        headers = kwargs.pop('headers', {})

        response = super().request(  # type: ignore
            method,
            url,
            verify=False,
            headers=headers,
            *args, **kwargs
        )
        self._check_for_error(response)
        return response

    def _check_for_error(self, response: Response) -> None:
        try:
            response.raise_for_status()

        except HTTPError:
            msg = textwrap.dedent(f"""
            ***Request***
                {response.status_code} {response.request.method} {response.url}
                Body: {str(response.request.body)}
                Headers: {response.request.headers}

            ***Response***
                Headers: {response.headers}
                Body: {response.text}""")

            self._logger.exception(msg)
            raise

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)
