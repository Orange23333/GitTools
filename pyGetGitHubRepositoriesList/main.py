# -*- coding: UTF-8 -*-

import getrepolist

if __name__ == '__main__':
	target = input("Target user or organization name: ")

	"""
	Output the target is a user or organization.
	"""
	account_type = getrepolist.get_account_type(target)
	if account_type == getrepolist.GitHubAccountType.USER:
		print("{} is user.".format(target))
	elif account_type == getrepolist.GitHubAccountType.ORGANIZATION:
		print("{} is organization.".format(target))
	else:
		print("Get account type failed. Please check your network.")
		raise ConnectionError("Get account type failed. Please check your network.", target)

	repo_name_list = getrepolist.get_repositories(target)
	print("[{}]".format(len(repo_name_list)))
	print(repo_name_list)

	"""
	check each repo is fork or not.
	"""
	for i in range(len(repo_name_list)):
		repo_json = getrepolist.get_repo(target, repo_name_list[i])
		is_fork = getrepolist.is_fork_repo(repo_json)
		print("{}. {} is fork? [{}]".format(i + 1, repo_name_list[i], is_fork))
