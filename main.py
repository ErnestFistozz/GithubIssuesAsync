import asyncio
from src.app.issues import GitHubIssuesMiner
from src.app.comments import GitHubCommentsMiner
from src.app.releases import GitHubReleaseMiner
from src.app.helpers import repositories, save_into_file


async def collect_issue_data(input_file: str, output: str) -> None:
    issue = []
    repos = repositories(input_file)
    if len(repos) != 0 and repos is not None:
        tasks = []
        for repo in repos:
            gh_issues_instance = GitHubIssuesMiner(repo[0], repo[1])
            task = asyncio.create_task(gh_issues_instance.gh_open_issues_miner())
            tasks.append(task)
        issue.extend(await asyncio.gather(*tasks))
        flat_data = [item for sublist in issue for item in sublist]
        save_into_file(output, flat_data)


async def collect_comment_data(input_file: str, output: str) -> None:
    issue = []
    repos = repositories(input_file)
    if len(repos) != 0 and repos is not None:
        tasks = []
        for repo in repos:
            gh_comments_instance = GitHubCommentsMiner(repo[0], repo[1])
            task = asyncio.create_task(gh_comments_instance.gh_issue_comments_miner())
            tasks.append(task)
        issue.extend(await asyncio.gather(*tasks))
        flat_data = [item for sublist in issue for item in sublist]
        save_into_file(output, flat_data)


async def collect_release_data(input_file: str, output: str) -> None:
    issue = []
    repos = repositories(input_file)
    if len(repos) != 0 and repos is not None:
        tasks = []
        for repo in repos:
            gh_releases_instance = GitHubReleaseMiner(repo[0], repo[1])
            task = asyncio.create_task(gh_releases_instance.gh_release_miner())
            tasks.append(task)
        issue.extend(await asyncio.gather(*tasks))
        flat_data = [item for sublist in issue for item in sublist]
        save_into_file(output, flat_data)


async def main(
        input_file='repositories.txt',
        issues_file='issues.csv',
        comments_file='comments.csv',
        release_files='releases.csv'
) -> None:
    await collect_issue_data(input_file, issues_file)
    await collect_release_data(input_file, comments_file)
    await collect_release_data(input_file, release_files)

if __name__ == '__main__':
    codecov_data = asyncio.get_event_loop().run_until_complete(main())
