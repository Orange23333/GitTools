# -*- coding: UTF-8 -*-

import json
import urllib.request

from enum import Enum


class GitHubAccountType(Enum):
	USER = 1
	ORGANIZATION = 2
	NAN = None


"""
Following is wrong, because it will return false if the internet is down. (Fully completed by the GitHub Copilot)
```
def is_a_github_user_or_org(github_account_name):
	" " "Check if a given name is a GitHub user or org." " "
	url = 'https://api.github.com/users/' + github_account_name
	request = urllib.request.Request(url)
	try:
		urllib.request.urlopen(request)
		return True
	except urllib.error.HTTPError:
		return False
```

Following I Added to fix the problem.
In the first case, it suggest me use `return True`.
But when I typed `return G`, it updated, and it suggest me use `return GitHubAccountType.USER`.
Except that, all the code is nearly completed by the GitHub Copilot.
"""
def get_account_type(github_account_name: str):
	"""
	Check if a given name is a GitHub user or org.
	:return: GitHubAccountType
	"""
	url = 'https://api.github.com/orgs/' + github_account_name
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	if response.getcode() == 200:
		return GitHubAccountType.ORGANIZATION
	else:
		url = 'https://api.github.com/users/' + github_account_name
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		if response.getcode() == 200:
			return GitHubAccountType.USER
		else:
			return GitHubAccountType.NAN


def get_user_repositories(user):
	"""
	Get a list of a user's repositories from GitHub API.
	:rtype: object
	"""
	url = 'https://api.github.com/users/{}/repos'.format(user)
	response = urllib.request.urlopen(url)
	data = json.loads(response.read().decode())
	return [repo['name'] for repo in data]


def get_org_repositories(org):
	"""List all names of GitHub repositories for an org.
	:rtype: object
	"""
	url = 'https://api.github.com/orgs/' + org + '/repos'
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	data = json.loads(response.read().decode())
	return [repo['name'] for repo in data]


"""
Following is wrong.
```
def get_repos(name):
	" " "List all names of GitHub repositories for a user or org.
	:rtype: object
	" " "
	url = 'https://api.github.com/users/' + name + '/repos'
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	data = json.loads(response.read().decode())
	return [repo['name'] for repo in data]
```

But when I guided it finished the `is_a_github_user_or_org` (also it is wrong),
I typed `def get_repositories(name)` again, and it completed this function.
"""
def get_repositories(name):
	"""List all names of GitHub repositories for a user or org.
	:rtype: object
	"""
	account_type = get_account_type(name)
	if account_type == GitHubAccountType.USER:
		return get_user_repositories(name)
	elif account_type == GitHubAccountType.ORGANIZATION:
		"""I don't know why, it use `else if` before. But when I try again, it had changed to `elif`."""
		return get_org_repositories(name)
	else:
		return None


def get_repo(author, repo_name):
	"""Get a repository from GitHub API."""
	url = 'https://api.github.com/repos/{}/{}'.format(author, repo_name)
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	return json.loads(response.read().decode())


def is_fork_repo(repo_json):
	"""Check if a repository is a fork."""
	return repo_json['fork']
