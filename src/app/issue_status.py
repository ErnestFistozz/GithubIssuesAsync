from enum import Enum

class IssueState(str, Enum):
    Open = 'open'
    Closed = 'closed'
    AllIssues = 'all'


if __name__ == '__main__':
    print(__name__)
