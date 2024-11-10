#!/bin/bash

check() {
	error_yn=$(read -p "$1" <<< /dev/stdin)
	case $error_yn in
		[Nn]* ) echo "Fix that, motherfucker!"; exit -1;;
		[Yy]* ) echo "Good."; break;;
		* ) echo "Sorry, can't recognize this bullshit";;
	esac
}

echo "Let's start with the memory allocations."
data=$(grep -n -o -P '^\+.*((alloc)|(dup)).*\(.*\)' $1)
while read -r line ; do
	echo -e "Found the following (possible) memory allocation:\n"
	echo ${line}
	echo -e "\n"
	check "Is possible memory allocation processed (y/n)?: "
done <<< "$data"
