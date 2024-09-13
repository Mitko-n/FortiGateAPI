import json
import logging
import requests
from requests.adapters import HTTPAdapter, Retry

logging.captureWarnings(True)

__version__ = "0.6.5"


class FGT:

    def __init__(self, host, name="admin", key=None, token=None, csrf=True):
        self._host = host
        self._name = name
        self._key = key
        self._token = token
        self._url_prefix = f"https://{self._host}"
        self._default_headers = {"Content-Type": "application/json"}
        self._retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 501, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "UPDATE"],
        )
        self._adapter = HTTPAdapter(max_retries=self._retry_strategy)
        self._session = requests.session()
        self._session.mount("https://", self._adapter)
        self._session.headers.update(self._default_headers)
        self._session.verify = False

        if key or token:
            self.login(name=name, key=key, token=token, csrf=csrf)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logout()

    def login(self, name=None, key=None, token=None, csrf=True):
        self.logout()
        username = name if name is not None else self._name
        secretkey = key if key is not None else self._key
        token = token if token is not None else self._token

        if secretkey:
            url = f"{self._url_prefix}/logincheck"
            data = {"username": username, "secretkey": secretkey}
            try:
                response = self._session.post(url, data=data)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                return {"status": "error", "message": "LOGIN failed", "data": str(e)}

            if "error" in response.text:
                return {"status": "error", "message": "LOGIN failed", "data": "Invalid credentials"}

            if csrf:
                self._update_csrf()
        elif token:
            self._token = token
            self._session.headers.update({"Authorization": f"Bearer {token}"})
        else:
            return {"status": "error", "message": "LOGIN failed", "data": "Either a key or a token must be provided"}

        return {"status": "success", "message": "Login successful", "data": None}

    def _update_csrf(self):
        csrf_cookie = next((cookie.value[1:-1] for cookie in self._session.cookies if cookie.name == "ccsrftoken"), None)
        if csrf_cookie:
            self._session.headers.update({"X-CSRFTOKEN": csrf_cookie})

    def logout(self):
        if self._session:
            url = f"{self._url_prefix}/logout"
            try:
                self._session.post(url)
            except requests.exceptions.RequestException as e:
                logging.error(f"Logout failed: {e}")
            finally:
                self._session.headers.pop("Authorization", None)
                self._session.close()

    def _request(self, method, url, **options):
        url = f"{self._url_prefix}{url}"
        headers = options.pop("headers", {})
        headers.update(self._default_headers)
        try:
            response = method(url, headers=headers, **options)
            response.raise_for_status()
            try:
                data = response.json()
            except ValueError:
                data = response.text
            return {"status": "success", "message": "Request successful", "data": data}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": "Request failed", "data": str(e)}

    def get(self, url, **options):
        return self._request(self._session.get, url, **options)

    def post(self, url, override=None, **options):
        data = options.get("data", {})
        if override:
            self._session.headers.update({"X-HTTP-Method-Override": override})
        response = self._request(self._session.post, url, params=options.get("params"), data=json.dumps(data), files=options.get("files"))
        if override:
            del self._session.headers["X-HTTP-Method-Override"]
        return response

    def put(self, url, **options):
        data = options.get("data", {})
        return self._request(self._session.put, url, params=options.get("params"), data=json.dumps(data), files=options.get("files"))

    def delete(self, url, **options):
        return self._request(self._session.delete, url, params=options.get("params"))
