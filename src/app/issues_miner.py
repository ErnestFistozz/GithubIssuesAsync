import requests
from src.app.base import GitHubIssueIUri
from src.app.issue_status import IssueState
from src.app.helpers import *
class RepositoryIssue(GitHubIssueIUri):

    def __init__(self, organisation, repository: str) -> None:
        super().__init__(organisation, repository)

    def gh_open_issues_miner(self, state: IssueState = 'all') -> list:
        empty = False
        page = 1
        all_issues = []
        uri = f'{super().url()}/issues?per_page=100&direction=asc'
        while not empty:
            try:
                uri = f'{uri}&state={state}&page={page}'
                issues = requests.get(uri, verify=False)
                issues.raise_for_status()
                issues = issues.json()
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
            except (KeyError, requests.exceptions.RequestException):
                pass
            page += 1
        return all_issues

    def issue_comments_miner(self) -> list:
        empty = False
        all_comments = []
        page = 1
        while not empty:
            uri = f'{super().uri()}/issues/comments?per_page=100&page={page}&direction=asc'
            try:
                comments = requests.get(uri, verify=False)
                comments.raise_for_status()
                comments = comments.json()
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
            except (KeyError, requests.exceptions.RequestException):
                pass
            page += 1
        return all_comments
