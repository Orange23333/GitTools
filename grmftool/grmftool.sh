#!/bin/bash

echo "Info: You could find any text your may need to replace by searching '#*'."
echo "Info: Sometimes, you need press times of Ctrl+C to stop the scripts."

echo "Debug: Warning that this script can't not check whether repository isn't exists!"
echo "Debug: Warning that this script can't not escape string for JSON file!"
#echo "Debug: Warning that this script can't queto with parameter to other program!"

auto_checkout_fetch_head = 1 #* # 0 as false, any number not 0 as true.

if [[ $# != 1 ]]; then
	echo "Error: Syntax error. Format: grmftool \"<user>/<repo_name>\""
	exit -1
fi

echo "Git Repository Mirror Fetch Tool v1.0 made by Orange233(https://github.com/Orange23333)"

begin_path=$PWD
git_mirror_root_dir="/d/Work/mirrors/git/github.com" #* #Here is your git mirror root directory. Without ending directory separator.
git_remote_url="https://github.com" #* #Here is your remote git root url. Without ending directory separator.
repo_dir=${1%/}
repo_dir=${repo_dir%\\}

#echo "\$0 = \"${0}\"."
echo "Track: begin_path = \"${begin_path}\"."
echo "Track: git_mirror_root_dir = \"${git_mirror_root_dir}\"."
echo "Track: git_remote_url = \"${git_remote_url}\"."
echo "Track: repo_dir = \"${repo_dir}\"."

echo "Debug: cd \"$git_mirror_root_dir\""
cd "$git_mirror_root_dir"
echo "Debug: mkdir -p \"$repo_dir\""
mkdir -p "$repo_dir"
echo "Debug: cd \"$repo_dir\""
cd "$repo_dir"

if [ ! -d ".git" ]; then
	echo "Debug: git init"
	git init
else
	echo "Warning: \".git\" has existed!"
fi

target_url="${git_remote_url}/${repo_dir}"
execute_result=""
while ! [[ $execute_result == 0 ]]; do
	echo "Debug: git fetch \"$target_url\""
	git fetch "$target_url"
	execute_result=$?
done;


if [[ ($auto_checkout_fetch_head == "") || ($auto_checkout_fetch_head == 0) ]]; then
	echo "Do \"git checkout FETCH_HEAD\"?[y/N] "
	read -r -n 1 user_answer
else
	user_answer='Y'
fi

if [[ ($user_answer == 'Y') || ($user_answer == 'y') ]]; then
	echo "git checkout FETCH_HEAD"
	git checkout FETCH_HEAD
	execute_result=$?

	if [[ $execute_result != 0 ]]; then
		error_msg="{\"Timestamp\": \"$(date --rfc-3339=seconds)\", \"ErrorType\": \"GitCheckoutFailed\", \"Data\": {\"RepositryDirctory\": \"${git_mirror_root_dir}/${repo_dir}\"}}"
	#	sed_cmd="\$ a ${error_msg}"
		sed_output_path="${begin_path}/grmftool.log"
	#	if [ ! -f "$sed_output_path" ]; then
	#		echo "Debug: touch \"$sed_output_path\""
	#		touch "$sed_output_path"
	#	fi
	#	echo "Debug: sed \"$sed_cmd\" \"$sed_output_path\""
	#	sed "$sed_cmd" "$sed_output_path"
		echo "Debug: echo \"$error_msg\" >> \"$sed_output_path\""
		echo "$error_msg" >> "$sed_output_path"

		exit -1
	fi
fi

exit 0
