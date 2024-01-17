from authlib.integrations.httpx_client import AsyncOAuth2Client, AsyncOAuth1Client
from authlib.integrations.base_client.async_app import AsyncOAuth2Mixin, AsyncOAuth1Mixin
from authlib.integrations.base_client import BaseOAuth, FrameworkIntegration
from social_core.strategy import BaseStrategy
import httpx


class OAuth2Strategy(BaseStrategy):
    """Dummy strategy for using the `BaseOAuth2.user_data` method."""

    def request_data(self, merge=True):
        return {}

    def absolute_uri(self, path=None):
        return path

    def get_setting(self, name):
        """Mocked setting method."""

    @staticmethod
    def get_json(url, method='GET', *args, **kwargs):
        return httpx.request(method, url, *args, **kwargs)

class AsyncOAuth1(AsyncOAuth1Mixin):
    client_cls = AsyncOAuth1Client

class AsyncOAuth2(AsyncOAuth2Mixin):
    client_cls = AsyncOAuth2Client

class FrameworkIntegration(FrameworkIntegration):
    @staticmethod
    def load_config(oauth, name, params):
        return {}

class OAuth(BaseOAuth):
    oauth1_client_cls = AsyncOAuth1
    oauth2_client_cls = AsyncOAuth2
    framework_integration_cls = FrameworkIntegration

    def __init__(self, config=None, cache=None, fetch_token=None, update_token=None):
        super().__init__(cache=cache, fetch_token=fetch_token, update_token=update_token)
        self.config = config

async def main():
    oauth = OAuth()

    oauth.register(
        name="google",
        client_id="692955511020-lgf2s9f9nmnhu9sfinhug6kmf5v3aafg.apps.googleusercontent.com",
        client_secret="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",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        access_token_url="https://accounts.google.com/o/oauth2/token",
        # server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        scope="openid profile email"
    )

    redirect_uri = "http://localhost:8000/auth/sso/google/callback"

    url = await oauth.google.create_authorization_url(redirect_uri=redirect_uri)
    print(url)

    token = await oauth.google.fetch_access_token(authorization_response=input("Enter URL: "))
    print(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
