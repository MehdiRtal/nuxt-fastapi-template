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

class AsyncOAuth1App(AsyncOAuth1Mixin):
    client_cls = AsyncOAuth1Client

class AsyncOAuth2App(AsyncOAuth2Mixin):
    client_cls = AsyncOAuth2Client

class FrameworkIntegration(FrameworkIntegration):
    @staticmethod
    def load_config(oauth, name, params):
        return {}

class OAuth(BaseOAuth):
    oauth1_client_cls = AsyncOAuth1App
    oauth2_client_cls = AsyncOAuth2App
    framework_integration_cls = FrameworkIntegration

    def __init__(self, config=None, cache=None, fetch_token=None, update_token=None):
        super().__init__(cache=cache, fetch_token=fetch_token, update_token=update_token)
        self.config = config

async def main():
    oauth = OAuth(config=OAuth2Strategy())

    oauth.register(
        name="google",
        client_id="377329661037-t2saf5e0g9lun78mst3515t432memqk9.apps.googleusercontent.com",
        client_secret="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",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        access_token_url="https://accounts.google.com/o/oauth2/token",
        scope="openid profile email"
    )

    redirect_uri = "http://localhost:8000/auth/sso/google/callback"

    url = await oauth.google.create_authorization_url(redirect_uri=redirect_uri)
    print(url)

    token = await oauth.google.fetch_access_token(redirect_uri=redirect_uri, authorization_response=input("Enter URL: "))
    access_token = token["access_token"]
    user_info = oauth.google.user_data(access_token)
    print(user_info)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
