from abc import ABC


class TostiAPIService(ABC):
    """Tosti API Service."""

    def __init__(self, base_url, client_id, client_secret, scope=None):
        """Initialize TOSTI API service."""
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope

        self.authorize_url = f"{base_url}/oauth/authorize/"
        self.token_url = f"{base_url}/oauth/token/"
        self.refresh_url = f"{base_url}/oauth/token/"

    @property
    def _client(self):
        """Get the client that takes care of authentication."""
        raise NotImplementedError()

    def get(self, path, *args, **kwargs):
        """Send GET request."""
        return self._client.get(f"{self.base_url}{path}", *args, **kwargs)

    def post(self, path, data, *args, **kwargs):
        """Send POST request."""
        return self._client.post(f"{self.base_url}{path}", data=data, *args, **kwargs)

    def put(self, path, data, *args, **kwargs):
        """Send PUT request."""
        return self._client.put(f"{self.base_url}{path}", data=data, *args, **kwargs)

    def patch(self, path, data, *args, **kwargs):
        """Send PATCH request."""
        return self._client.patch(f"{self.base_url}{path}", data=data, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        """Send DELETE request."""
        return self._client.delete(f"{self.base_url}{path}", *args, **kwargs)

    def head(self, path, *args, **kwargs):
        """Send HEAD request."""
        return self._client.head(f"{self.base_url}{path}", *args, **kwargs)

    def options(self, path, *args, **kwargs):
        """Send OPTIONS request."""
        return self._client.options(f"{self.base_url}{path}", *args, **kwargs)
