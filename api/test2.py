from authlib.integrations.httpx_client import AsyncOAuth2Client
import httpx

async def main():
    client = AsyncOAuth2Client(
        client_id="377329661037-t2saf5e0g9lun78mst3515t432memqk9.apps.googleusercontent.com",
        client_secret="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",
        redirect_uri="http://localhost:8000/auth/sso/google/callback",
        scope="openid profile email"
    )
    url, _ = client.create_authorization_url("https://accounts.google.com/o/oauth2/auth")

    print(url)

    token = await client.fetch_token("https://accounts.google.com/o/oauth2/token", authorization_response=input("Enter URL: "))

    print(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
