import aiohttp
from src.app.base import GitHubIssueIUri
from src.app.issue_status import IssueState

class GitHubIssuesMiner(GitHubIssueIUri):
    def __init__(self, organisation, repository: str) -> None:
        super().__init__(organisation, repository)

    async def gh_open_issues_miner(self, state=IssueState.Closed):
        empty = False
        page = 1
        all_issues = []
        async with aiohttp.ClientSession() as session:
            while not empty:
                try:
                    uri = f'{self.uri()}/issues?per_page=100&direction=asc&state={state}&page={page}'
                    issues = await super().fetch_data(session, uri)
                    if issues:
                        for issue in issues:
                            current_issue = {
                                "repository": f"{self.organisation}/{self.repository}",
                                "issue_id": issue['id'],
                                "issue_number": issue['number'],
                                "labels": "" if not issue['labels'] else ",".join(
                                    [label['name'] for label in issue['labels']]),
                                "status": issue['state'],
                                "comments": int(issue['comments']),
                                "created_at": issue['created_at'],
                                "updated_at": issue['updated_at'],
                                "closed_at": issue['closed_at'],
                                "issue_title": issue['title'],
                                "state_reason": issue['state_reason'],
                                "assigned": False if not issue['assignee'] else True,
                                "number_of_assignees": 0 if not issue['assignee'] else len(issue['assignee']),
                            }
                            all_issues.append(current_issue)
                    else:
                        empty = True
                except (KeyError, aiohttp.ClientError) as e:
                    pass
                page += 1
        return all_issues
