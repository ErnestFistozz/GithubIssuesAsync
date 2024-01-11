import aiohttp
import asyncio
from src.app.helpers import *

class GitHubIssueIUri:
    def __init__(self, organisation: str, repository: str) -> None:
        self.organisation = organisation
        self.repository = repository
        self.uri = f'https://api.github.com/repos/{self.organisation}/{self.repository}'

    def org(self) -> str:
        return self.organisation

    def repo(self) -> str:
        return self.repository

    def url(self) -> str:
        return self.uri

    async def fetch_data(self, session, uri):
        async with session.get(uri) as response:
            if response.status == 200:
                return await response.json()
            elif response.status in [403, 429]:
                retry_after = convert_utc_epoch_to_seconds(int(response.headers.get('x-ratelimit-reset', '60')))
                await asyncio.sleep(retry_after)
                return await self.fetch_data(session, uri)
            else:
                return None
