#!/bin/python3
# -*- coding: UTF-8 -*-

import getrepolist

if __name__ == '__main__':
	target = input("Target user or organization name: ")

	repo_name_list = getrepolist.get_repositories(target)
	print("[{}]".format(len(repo_name_list)), end='')
	print(repo_name_list)
