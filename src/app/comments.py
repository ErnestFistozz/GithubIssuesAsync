import aiohttp
from src.app.base import GitHubIssueIUri

class GitHubCommentsMiner(GitHubIssueIUri):
    def __init__(self, organisation, repository: str) -> None:
        super().__init__(organisation, repository)

    async def gh_issue_comments_miner(self) -> list:
        empty = False
        all_comments = []
        page = 1
        async with aiohttp.ClientSession() as session:
            while not empty:
                uri = f'{self.url()}/issues/comments?per_page=100&page={page}&direction=asc'
                try:
                    comments = await super().fetch_data(session, uri)
                    if comments:
                        for comment in comments:
                            issue_comment = {
                                "repository": f"{self.organisation}/{self.repository}",
                                "issue_id": comment['issue_url'].split('/')[-1],
                                "comment_id": comment['id'],
                                "created_at": comment['created_at'],
                                "updated_at": comment['updated_at'],
                                "comment_msg": "" if not comment['body'] else ",".join(
                                    [currentComment for currentComment in comment['body']])
                            }
                            all_comments.append(issue_comment)
                    else:
                        empty = True
                except (KeyError, aiohttp.ClientError):
                    pass
                page += 1
        return all_comments
