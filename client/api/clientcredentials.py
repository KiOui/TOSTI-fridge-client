from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from api.apiservice import TostiAPIService


class TostiClientCredentialsAPIService(TostiAPIService):
    """Client Credentials API Service for TOSTI."""

    def __init__(self, *args, **kwargs):
        """Initialize Tosti Client Credentials API Service."""
        super().__init__(*args, **kwargs)
        self._token = None

    def _get_token(self):
        """Get a new OAuth 2.0 token."""
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client, scope=self.scope)

        self._token = oauth.fetch_token(
            token_url=self.token_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope,
        )

    @property
    def token(self):
        """Get the token."""
        return self._token

    @token.setter
    def token(self, token):
        """Set the token."""
        self._token = token

    @property
    def _client(self):
        """Get the client."""
        if self._token is None:
            self._get_token()
        return OAuth2Session(
            self.client_id,
            token=self._token,
            auto_refresh_url=self.refresh_url,
            token_updater=self.token,
        )
