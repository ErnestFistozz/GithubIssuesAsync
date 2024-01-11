import aiohttp
from src.app.base import GitHubIssueIUri

class GitHubReleaseMiner(GitHubIssueIUri):
    def __init__(self, organisation: str, repository: str) -> None:
        super().__init__(organisation, repository)

    async def gh_release_miner(self) -> list:
        empty = False
        all_releases = []
        page = 1
        async with aiohttp.ClientSession() as session:
            while not empty:
                uri = f'{super().uri()}/releases?per_page=100&page={page}&direction=asc'
                try:
                    releases = await super().fetch_data(session, uri)
                    if releases:
                        for release in releases:
                            gh_release = {
                                "repository": f"{self.organisation}/{self.repository}",
                                "release_id": release['id'],
                                "tag_name": release['tag_name'],
                                "target_commitish": release['target_commitish'],
                                "release_name": release['name'],
                                "published_at": release['published_at'],
                                "created_at": release['created_at'],
                                "release_msg": release['body']
                            }
                            all_releases.append(gh_release)
                    else:
                        empty = True
                except (KeyError, aiohttp.ClientError):
                    pass
                page += 1
        return all_releases
