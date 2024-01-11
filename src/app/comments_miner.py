import aiohttp
import asyncio
from src.app.base import GitHubIssueIUri
from src.app.helpers import *
class IssueComments(GitHubIssueIUri):
    def __init__(self, organisation, repository: str) -> None:
        super().__init__(organisation, repository)

    async def fetch_github_comments(self, session, url, page, retry_attempts=3):
        params = {'page': page, 'per_page': 100}
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            elif response.status in [429, 403]:  # Check for rate limit exceeded
                rem_time = int(response.headers.get('x-ratelimit-reset', '0'))
                retry_after = convert_utc_epoch_to_seconds(rem_time)
                if retry_after > 0:
                    print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    await asyncio.sleep(retry_after)
                    return await self.fetch_github_comments(session, url, page)
                else:
                    await asyncio.sleep(2 ** retry_attempts)
                    return await self.fetch_github_comments(session, url, page)
            else:
                return {}

    async def fetch_all_comments(self, url):
        all_issues = []
        async with aiohttp.ClientSession() as session:
            page = 1
            while True:
                try:
                    data = await self.fetch_github_comments(session, url, page)
                    if not data:
                        break  # No more issues
                    all_issues.extend(data)
                    page += 1
                except Exception:
                    continue
        return all_issues

    async def main(self):
        issues = await self.fetch_all_comments(self.url())
        return issues


if __name__ == "__main__":
    comments = IssueComments('', '')
    asyncio.run(comments.main())
